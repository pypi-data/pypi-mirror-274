import datetime
import os
import time
from typing import Literal
import pandas as pd
import plotly.express as px
import tabulate
from wiliot_deployment_tools.ag.ut_defines import BRIDGE_ID, NFPKT, PAYLOAD, RSSI, LAT, LNG
from wiliot_deployment_tools.api.extended_api import GatewayType
from wiliot_deployment_tools.common.debug import debug_print
from wiliot_deployment_tools.gw_certificate.api_if.gw_capabilities import GWCapabilities
from wiliot_deployment_tools.gw_certificate.tests.static.coupling_defines import INCREMENTAL_STAGE_ADVA
from wiliot_deployment_tools.interface.ble_simulator import BLESimulator
from wiliot_deployment_tools.interface.if_defines import BRIDGES, DEFAULT_DELAY, LOCATION
from wiliot_deployment_tools.interface.uart_if import UARTInterface
from wiliot_deployment_tools.gw_certificate.tests.static.uplink_defines import *
from wiliot_deployment_tools.interface.mqtt import MqttClient
from wiliot_deployment_tools.interface.pkt_generator import BrgPktGenerator, BrgPktGeneratorNetwork, TagPktGenerator
from wiliot_deployment_tools.gw_certificate.tests.static.generated_packet_table import TEST_COUPLING, TEST_UPLINK, TEST_UNIFIED, CouplingRunData, UplinkRunData, UnifiedRunData
from wiliot_deployment_tools.gw_certificate.tests.generic import PassCriteria, PERFECT_SCORE, MINIMUM_SCORE, INCONCLUSIVE_MINIMUM, INIT_INCONCLUSIVE_MINIMUM, GenericTest, GenericStage
from wiliot_deployment_tools.interface.packet_error import PacketError
from wiliot_deployment_tools.gw_certificate.api_if.api_validation import MESSAGE_TYPES, validate_message
from wiliot_deployment_tools.gw_certificate.tests.static.generated_packet_table import CSV_NAME
import pkg_resources


# TEST STAGES

class UplinkTestError(Exception):
    pass

class GenericUplinkStage(GenericStage):
    def __init__(self, mqttc:MqttClient, ble_sim:BLESimulator, gw_capabilities:GWCapabilities, stage_name,
                **kwargs):
        self.__dict__.update(kwargs)
        super().__init__(stage_name=stage_name, **self.__dict__)
                
        # Clients
        self.mqttc = mqttc
        self.ble_sim = ble_sim

        # Packets list
        self.local_pkts = []
        self.mqtt_pkts = []
        
        # GW Capabilities
        self.gw_capabilities = gw_capabilities
        
        # Packet Error / Run data
        self.packet_error = PacketError()
        self.run_data = CouplingRunData if self.coupled else UplinkRunData
        
        # Unified stage
        self.run_data_unified = UnifiedRunData

        # Data extracted from the test csv
        self.all_test_payloads = None
        self.alias_bridge_id_df = None
    
    def prepare_stage(self, reset_ble_sim=True):
        super().prepare_stage()
        self.mqttc.flush_messages()
        if reset_ble_sim:
            self.ble_sim.set_sim_mode(True) 
        
    def fetch_mqtt_from_stage(self):
        def process_payload(packet:dict):
            payload = packet[PAYLOAD]
            payload = payload.upper()
            if len(payload) == 62:
                if payload[:4] == '1E16':
                    payload = payload [4:]
            # big2little endian
            if payload[:4] == 'FCC6':
                payload = 'C6FC' + payload[4:]
            packet[PAYLOAD] = payload
            return packet
        mqtt_pkts = self.mqttc.get_all_tags_pkts()
        self.mqtt_pkts = list(map(lambda p: process_payload(p), mqtt_pkts))
    
    ## TODO - REWRITE
    def compare_local_mqtt(self):
        self.fetch_mqtt_from_stage()
        local_pkts_df = pd.DataFrame(self.local_pkts)
        mqtt_pkts_df = pd.DataFrame(self.mqtt_pkts)
        comparison = local_pkts_df

        # Coupled
        if self.coupled:
            if not set(SHARED_COLUMNS) <= set(mqtt_pkts_df.columns):
                missing_columns = list(set(SHARED_COLUMNS) - set(mqtt_pkts_df.columns))
                for missing_column in missing_columns:
                    if missing_column in OBJECT_COLUMNS:
                        mqtt_pkts_df[missing_column] = ''
                    if missing_column in INT64_COLUMNS:
                        mqtt_pkts_df[missing_column] = 0
            received_pkts_df = pd.merge(local_pkts_df[SHARED_COLUMNS], mqtt_pkts_df[SHARED_COLUMNS], how='inner')
        # Uncoupled
        else:
            if PAYLOAD not in mqtt_pkts_df.columns:
                mqtt_pkts_df[PAYLOAD] = ''
            received_pkts_df = pd.merge(local_pkts_df[PAYLOAD], mqtt_pkts_df[PAYLOAD], how='inner')
        
        received_pkts = set(received_pkts_df[PAYLOAD])

        self.pkts_received_count = pd.Series.count(received_pkts_df)
        unique_received_count = len(received_pkts)
        self.pkts_filtered_out_count = self.pkts_received_count - unique_received_count

        comparison[RECEIVED] = comparison[PAYLOAD].isin(received_pkts)
        comparison['pkt_id'] = comparison['payload'].apply(lambda x: x[-8:])
        self.comparison = comparison
                
    def generate_stage_report(self):
        """
        Generates report for the stage
        """
        self.compare_local_mqtt()
        report = []
        num_pkts_sent = len(self.comparison)
        num_pkts_received = self.comparison['received'].eq(True).sum()
        self.stage_pass = num_pkts_received / num_pkts_sent * PERFECT_SCORE
        self.stage_pass = PassCriteria.calc_for_stage_uplink(self.stage_pass, self.stage_name)

        report.append(((f'Number of {"coupled" if self.coupled else "unique"} packets sent'), num_pkts_sent))
        report.append(((f'Number of {"coupled" if self.coupled else "unique"} packets received'), num_pkts_received))
        report.append(((f'Number of total packets received'), self.pkts_received_count))
        report.append(((f'Number of duplicates out of total'), self.pkts_filtered_out_count))
        self.add_to_stage_report(f'---Stage {self.stage_name} {PassCriteria.to_string(self.stage_pass)}, Running time {datetime.datetime.now() - self.start_time}')
        self.add_to_stage_report(tabulate.tabulate(pd.DataFrame(report), showindex=False))
        not_received = self.comparison[self.comparison[RECEIVED]==False][REPORT_COLUMNS]
        if len(not_received) > 0:
            self.add_to_stage_report('Packets not received:')
            self.add_to_stage_report(tabulate.tabulate(not_received, headers='keys', showindex=False))
        self.comparison.to_csv(self.csv_path)
        self.add_to_stage_report(f'Stage data saved - {self.csv_path}')
        debug_print(self.report)
        
        # Generate HTML
        table_html = self.template_engine.render_template('table.html', dataframe=self.comparison.to_html(table_id=self.stage_name), table_id=self.stage_name)
        self.report_html = self.template_engine.render_template('stage.html', stage_name = self.stage_name, stage_pass=self.stage_pass, 
                                                                pass_min=self.pass_min, inconclusive_min=self.inconclusive_min, 
                                                                stage_report=self.report.split('\n'), table=table_html)
        
        return self.report
    
# Uncoupled Stages

class InitStage(GenericUplinkStage):
    
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)
        super().__init__(**self.__dict__, stage_name=type(self).__name__)
        self.pkt_gen = BrgPktGenerator(bridge_id=UPLINK_BRG_ID)
    
    def run(self):
        self.start_time = datetime.datetime.now()
        for duplication in INIT_STAGES_DUPLICATIONS:
            self.pkt_gen.increment_all()
            pkt = self.pkt_gen.get_brg_hb()
            expected = self.pkt_gen.get_expected_hb_mqtt()
            expected.update({'duplication': duplication, 'time_delay': DEFAULT_DELAY})
            self.local_pkts.append(expected)
            self.ble_sim.send_packet(raw_packet=pkt, duplicates=duplication, delay=DEFAULT_DELAY)
        time.sleep(5)

class BrgDataStage(GenericUplinkStage):
    
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)
        super().__init__(**self.__dict__, stage_name=type(self).__name__)
        self.pkt_gen = BrgPktGenerator()
    
    
    def run(self):
        self.start_time = datetime.datetime.now()
        for duplication in UPLINK_DUPLICATIONS:
            debug_print(f'Duplication {duplication}')
            for time_delay in UPLINK_TIME_DELAYS:
                debug_print(f'Time Delay {time_delay}')
                run_data = self.run_data.get_data(TEST_UPLINK, duplication, time_delay, BRIDGES[0])
                data = run_data.data
                si = run_data.si
                self.local_pkts.extend(run_data.expected_mqtt)
                self.ble_sim.send_data_si_pair(data, si, duplication, delay=time_delay)
        time.sleep(5)

# Unified Stages
class OneBrgUnifiedPacketStage(GenericUplinkStage):
# currently only one bridge is simulated. If we want to simulate more, then make sure that they have different parameters to send (rssi,nfpkt,latency,global pacing group)
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)
        super().__init__(**self.__dict__, stage_name=type(self).__name__)
        self.pkt_gen = BrgPktGenerator()

    def run(self):
        self.start_time = datetime.datetime.now()
        for duplication in UNIFIED_DUPLICATIONS:
            debug_print(f'Duplication {duplication}')
            for time_delay in UNIFIED_TIME_DELAYS:
                debug_print(f'Time Delay {time_delay}')
                run_data = self.run_data_unified.get_data(TEST_UNIFIED, duplication, time_delay, BRIDGES[0])
                data = run_data.data
                self.local_pkts.extend(run_data.expected_mqtt)
                for dup in range(duplication):
                    self.ble_sim.send_packet(data, duplicates=1, delay=time_delay)
            time.sleep(5)

class ThreeBrgUnifiedPacketStage(GenericUplinkStage):  

    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)
        super().__init__(**self.__dict__, stage_name=type(self).__name__)
        self.brg_network = BrgPktGeneratorNetwork()
    
    def run(self):
        self.start_time = datetime.datetime.now()
        for duplication in UNIFIED_DUPLICATIONS:
            debug_print(f'Duplication {duplication}')
            for time_delay in UNIFIED_TIME_DELAYS:
                debug_print(f'Time Delay {time_delay}')
                # Construct packet list from data
                pkts = []
                for brg_idx in BRIDGES:
                    pkt = {}
                    run_data = self.run_data_unified.get_data(TEST_UNIFIED, duplication, time_delay, brg_idx)
                    pkt['data_packet'] = run_data.data
                    pkt['bridge_id'] = run_data.bridge_id
                    self.local_pkts.extend(run_data.expected_mqtt)
                    pkts.append(pkt)
                # Send packets
                self.ble_sim.send_brg_network_pkts_unified(pkts, duplication, delay=time_delay)
        time.sleep(5)

# Coupled Stages
class CoupledInitStage(GenericUplinkStage):
    
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)
        super().__init__(**self.__dict__, stage_name=type(self).__name__)
        self.pkt_gen = BrgPktGenerator()
    
    def run(self):
        self.start_time = datetime.datetime.now()
        for idx, duplication in enumerate(INIT_STAGES_DUPLICATIONS):
            new_pkt = self.pkt_gen.get_new_data_si()
            # First 2 runs generate smallest RSSI/NFPKT
            # Last 2 runs generate biggest RSSI/NFPKT
            if idx < 2:
                self.pkt_gen.set_rssi_nfpkt(rssi=idx, nfpkt=idx)
            else:
                self.pkt_gen.set_rssi_nfpkt(rssi=MAX_RSSI-idx+2, nfpkt=MAX_NFPKT-idx+2)
            new_pkt = self.pkt_gen.get_existing_data_si()
            expected_pkt = self.pkt_gen.get_expected_coupled_mqtt()
            data = new_pkt['data_packet']
            si = new_pkt['si_packet']
            expected_pkt.update({'duplication': duplication, 'time_delay': DEFAULT_DELAY,
            'si_rawpacket': si, 'data_rawpacket': data})
            self.local_pkts.append(expected_pkt)
            self.ble_sim.send_data_si_pair(data, si, duplication, delay=DEFAULT_DELAY)
        time.sleep(5)
class CoupledOneBrgStage(GenericUplinkStage):
    
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)
        super().__init__(**self.__dict__, stage_name=type(self).__name__)
        self.pkt_gen = BrgPktGenerator()
    
    def run(self):
        self.start_time = datetime.datetime.now()
        for duplication in COUPLING_DUPLICATIONS:
            debug_print(f'Duplication {duplication}')
            for time_delay in COUPLING_TIME_DELAYS:
                debug_print(f'Time Delay {time_delay}')
                run_data = self.run_data.get_data(TEST_COUPLING, duplication, time_delay, BRIDGES[0])
                data = run_data.data
                si = run_data.si
                packet_error = run_data.packet_error
                self.local_pkts.append(run_data.expected_mqtt)
                self.ble_sim.send_data_si_pair(data, si, duplication, delay=time_delay, packet_error=packet_error)
        time.sleep(5)

class CoupledThreeBrgInitStage(GenericUplinkStage):
    
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)
        super().__init__(**self.__dict__, stage_name=type(self).__name__)
        self.brg_network = BrgPktGeneratorNetwork()
    
    def run(self):
        self.start_time = datetime.datetime.now()
        duplication = COUPLING_DUPLICATIONS[3]
        time_delay = COUPLING_TIME_DELAYS[2]
        # Construct packet list from data
        pkts = []
        for brg_idx in BRIDGES:
            pkt = {}
            run_data = self.run_data.get_data(TEST_COUPLING, duplication, time_delay, brg_idx)
            pkt['data_packet'] = run_data.data
            pkt['si_packet'] = run_data.si
            pkt['time_delay'] = run_data.scattered_time_delay
            pkt['packet_error'] = run_data.packet_error
            pkt['bridge_id'] = run_data.bridge_id
            self.local_pkts.append(run_data.expected_mqtt)
            pkts.append(pkt)
        # Send scattered packets
        self.ble_sim.send_brg_network_pkts(pkts, duplication)
        time.sleep(5)
        


class CoupledThreeBrgStage(GenericUplinkStage):
    
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)
        super().__init__(**self.__dict__, stage_name=type(self).__name__)
        self.brg_network = BrgPktGeneratorNetwork()
    
    def run(self):
        self.start_time = datetime.datetime.now()
        for duplication in COUPLING_DUPLICATIONS:
            debug_print(f'Duplication {duplication}')
            # Time delays from 45 -> 255
            for time_delay in COUPLING_TIME_DELAYS[1:]:
                debug_print(f'Time Delay {time_delay}')
                # Construct packet list from data
                pkts = []
                for brg_idx in BRIDGES:
                    pkt = {}
                    run_data = self.run_data.get_data(TEST_COUPLING, duplication, time_delay, brg_idx)
                    pkt['data_packet'] = run_data.data
                    pkt['si_packet'] = run_data.si
                    pkt['time_delay'] = run_data.scattered_time_delay
                    pkt['packet_error'] = run_data.packet_error
                    pkt['bridge_id'] = run_data.bridge_id
                    self.local_pkts.append(run_data.expected_mqtt)
                    pkts.append(pkt)
                # Send scattered packets
                self.ble_sim.send_brg_network_pkts(pkts, duplication)
        time.sleep(5)

class ApiValidationStage(GenericUplinkStage):
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)
        super().__init__(**self.__dict__, stage_name=type(self).__name__)
    
    def prepare_stage(self):
        super().prepare_stage(reset_ble_sim=False)
        self.mqttc.flush_messages()

    def run(self):
        pass

    def get_data_from_test_csv(self):
        relative_path = 'static/' + CSV_NAME
        csv_path = pkg_resources.resource_filename(__name__, relative_path)
        df = pd.read_csv(csv_path)

        # Store all test payloads
        all_payloads = df['data'].str[12:]
        self.all_test_payloads = all_payloads.tolist()

        # Create data set for alias bridge verification
        alias_bridge_id_df = df[df['test'] == 'unified']
        alias_bridge_id_df['payload'] = alias_bridge_id_df['data'].str[12:]
        alias_bridge_id_df['alias_bridge_id'] = alias_bridge_id_df['data'].str[:12]
        # Convert bridge_id to little endian:
        alias_bridge_id_df['alias_bridge_id'] = alias_bridge_id_df['alias_bridge_id'].apply(lambda x: ''.join(format(byte, '02X') for byte in bytes.fromhex(x)[::-1]))
        self.alias_bridge_id_df = alias_bridge_id_df 
   
    def generate_stage_report(self, **kwargs):
        report = []
        all_validations = []
        self.stage_pass = PERFECT_SCORE
        self.get_data_from_test_csv()
        required_sequenceId = None
        sequenceId_valid = True
        aliasBridgeId_valid = True

        def get_message_data_type(message):
            if message.is_unified: 
                return 'unified'
            else:
                return 'legacy'
            
        def filter_non_test_packets(message):
            packets = message['packets']
            for pkt in packets[:]:
                payload = pkt['payload']
                if payload not in (self.all_test_payloads):
                    packets.remove(pkt)
                    message['packets'] = packets
                    
        def is_sequenceId_incremental(idx, message):
            nonlocal required_sequenceId, sequenceId_valid
            packets = message['packets']

            # initialize the required sequenceId 
            if idx == 0:
                first_pkt = packets[0]
                required_sequenceId = first_pkt['sequenceId'] 
            
            # check that for every packet in message the sequenceId is incremental:
            for pkt in packets:
                pkt_sequenceId = pkt['sequenceId']
                if pkt_sequenceId != required_sequenceId:
                    report.append(f'SequenceId is not incremental. The required sequenceId is {required_sequenceId} but the packet sequenceId is {pkt_sequenceId}')
                    self.stage_pass = MINIMUM_SCORE
                    sequenceId_valid = False
                required_sequenceId += 1

        def is_alias_bridge_id_valid(message): 
            nonlocal aliasBridgeId_valid
            packets = message['packets']

            for pkt in packets:
                if 'aliasBridgeId' in pkt: 
                    pkt_payload = pkt['payload']
                    pkt_alias_bridge_id = pkt['aliasBridgeId']
                    validation_data = self.alias_bridge_id_df[self.alias_bridge_id_df['payload']==pkt_payload] 
                    required_bridge_id = validation_data['alias_bridge_id'].iloc[0]
                    if pkt_alias_bridge_id != (required_bridge_id):
                        report.append(f"Alias bridge ID of the packet does not match. The required alias bridge ID is {required_bridge_id} but the packet alias bridge ID is {pkt_alias_bridge_id}")
                        self.stage_pass = MINIMUM_SCORE
                        aliasBridgeId_valid = False 

        # Set message type according to coupling, location
        for idx, message in enumerate(self.all_messages_in_test):
            message_body = message.body
            is_sequenceId_incremental(idx=idx, message=message_body)
            filter_non_test_packets(message_body)
            if len(message_body['packets']) == 0:
                continue
            is_alias_bridge_id_valid(message=message_body)
            validation = validate_message(MESSAGE_TYPES.DATA, message_body, get_message_data_type(message))
            all_validations.append({'valid':validation[0], 'error': validation[1], 'message': message_body,})
            validation_error = f'- {validation[1]}'
            if not validation[0] and validation_error not in report:
                if 'Validation Errors:' not in report:
                    report.append('Validation Errors:')
                report.append(validation_error + f'- message index {idx}')
                self.stage_pass = MINIMUM_SCORE

        # Set stage as FAIL if no messages were received:
        if len(self.all_messages_in_test) == 0:
            self.stage_pass = MINIMUM_SCORE

        self.add_to_stage_report(f'---Stage {self.stage_name} {PassCriteria.to_string(self.stage_pass)}')
        self.add_to_stage_report(f"{'---SequenceId is incremental' if sequenceId_valid else '---SequenceId is NOT incremental'}")
        self.add_to_stage_report(f"{'---Alias bridge ID is valid' if aliasBridgeId_valid else '---Alias bridge ID is NOT valid'}")
        # Add all messages that failed to validate to report
        for line in report:
            self.add_to_stage_report(line)
        all_validations_df = pd.DataFrame(all_validations)
        all_validations_df.to_csv(self.csv_path)
        self.add_to_stage_report(f'Stage data saved - {self.csv_path}')
        debug_print(self.report)
        
        #Generate HTML
        table_html = self.template_engine.render_template('table.html', dataframe=all_validations_df.to_html(table_id=self.stage_name), table_id=self.stage_name)
        self.report_html = self.template_engine.render_template('stage.html', stage_name = self.stage_name, stage_pass=self.stage_pass, 
                                                                pass_min=self.pass_min, inconclusive_min=self.inconclusive_min, 
                                                                stage_report=self.report.split('\n'), table=table_html)
        return self.report

class GeolocationStage(GenericUplinkStage):
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)
        super().__init__(**self.__dict__, stage_name=type(self).__name__)
        self.graph_html_path = os.path.join(self.test_dir, f'{self.stage_name}.html')

    
    def prepare_stage(self):
        super().prepare_stage(reset_ble_sim=False)
        self.mqttc.flush_messages()

    def run(self):
        pass
    
    def generate_stage_report(self, **kwargs):
        locations_list = []
        locations_df = pd.DataFrame()
        self.stage_pass = MINIMUM_SCORE

        # Set message type according to coupling, location
        for message in self.all_messages_in_test:
            message = message.body
            timestamp = message[TIMESTAMP]
            if LOCATION in message.keys():
                loc = message[LOCATION]
                loc.update({TIMESTAMP:timestamp})
                locations_list.append(loc)
        num_unique_locs = 0
        if len(locations_list) > 0:
            self.stage_pass = PERFECT_SCORE
            locations_df = pd.DataFrame(locations_list)
            num_unique_locs = locations_df[['lat', 'lng']].drop_duplicates().shape[0]
            fig = px.scatter_mapbox(locations_df, lat=LAT, lon=LNG, color='timestamp', zoom=10)
            fig.update(layout_coloraxis_showscale=False)
            fig.update_layout(scattermode="group", scattergap=0.95, mapbox_style="open-street-map")

        self.add_to_stage_report(f'---Stage {self.stage_name} {PassCriteria.to_string(self.stage_pass)}')
        self.add_to_stage_report(f'Number of unique locations received: {num_unique_locs}')
        # Export all stage data
        locations_df.to_csv(self.csv_path)
        self.add_to_stage_report(f'Stage data saved - {self.csv_path}')
        if num_unique_locs > 0:
            fig.write_html(self.graph_html_path)
        debug_print(self.report)
        
        #Generate HTML
        graph_div = fig.to_html(full_html=False, include_plotlyjs='cdn') if num_unique_locs > 0 else "No graph to display"
        self.report_html = self.template_engine.render_template('stage.html', stage_name = self.stage_name, stage_pass=self.stage_pass, 
                                                                pass_min=self.pass_min, inconclusive_min=self.inconclusive_min, 
                                                                stage_report=self.report.split('\n'), graph = graph_div)
        return self.report


# TEST CLASS
UNCOUPLED_STAGES = [InitStage, BrgDataStage, OneBrgUnifiedPacketStage, ThreeBrgUnifiedPacketStage, ApiValidationStage, GeolocationStage] 
COUPLED_STAGES = [CoupledInitStage, CoupledOneBrgStage, CoupledThreeBrgInitStage, CoupledThreeBrgStage, ApiValidationStage, GeolocationStage]

class UplinkTest(GenericTest):
    def __init__(self, **kwargs):        
        self.__dict__.update(kwargs)
        super().__init__(**self.__dict__, test_name=type(self).__name__)
        self.all_messages_in_test = []
        stages = COUPLED_STAGES if self.coupled else UNCOUPLED_STAGES
        self.stages = [stage(**self.__dict__) for stage in stages]
        

    def run(self):
        super().run()
        self.test_pass = PERFECT_SCORE
        for stage in self.stages:
            stage.prepare_stage()
            stage.run()
            self.add_to_test_report(stage.generate_stage_report())
            self.test_pass = PassCriteria.calc_for_test(self.test_pass, stage.stage_pass, stage.stage_name)
            self.all_messages_in_test.extend(self.mqttc.get_all_messages_from_topic('data'))
    
