import os
import json
from jsonschema import validate
from wiliot_deployment_tools.ag.ut_defines import GW_CONF, GW_API_VERSION
from wiliot_deployment_tools.common.debug import debug_print
import pkg_resources

from enum import Enum

class MESSAGE_TYPES(Enum):
    STATUS = "status"
    DATA = "data"
    LOGS = "logs"

# TODO Can we use GW_API_VER_DEFAULT from ag.ut_defines instead after we auto-generate again?
LATEST_API = "202"
api_version = LATEST_API

def validate_message(message_type: MESSAGE_TYPES, message: dict, data_type: str) -> tuple[bool, str]:
    """
    Validate MQTT message
    :type message_type: MESSAGE_TYPES
    :param message_type: MQTT message type
    :type message: dict
    :param message: MQTT Message
    :type data_type: str
    :param data_type: unified/legacy
    :return: tuple (bool, str)
    """
    global api_version

    # NOTE When Connection test is not ran (using the -tests flag), default api_version is the latest
    if message_type == MESSAGE_TYPES.STATUS:
        api_version = message[GW_CONF][GW_API_VERSION]
        debug_print(f'API version set as {api_version} according to the status message.')

    if message_type == MESSAGE_TYPES.DATA and data_type != None:
        json_path = pkg_resources.resource_filename(__name__, f"{api_version}/{message_type.value}_{data_type}.json")
    else:
        json_path = pkg_resources.resource_filename(__name__, f"{api_version}/{message_type.value}.json")
    with open(json_path) as f:
        schema = json.load(f)
    try:
        validate(message, schema)
        return (True, None)
    except Exception as e:
        return (False, e.message)