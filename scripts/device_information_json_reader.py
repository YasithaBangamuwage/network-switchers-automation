import json
import os
import logging
import logging.handlers as handlers
import sys
from datetime import date, timedelta
from log_utils import device_information_log_handler


exe_file = sys.executable
exe_parent = os.path.dirname(exe_file)
dir_path = os.path.dirname(exe_file)
#dir_path = os.path.dirname(os.path.realpath(__file__))
logger = logging.getLogger(__name__)


def initialize_device_information_logger():
    logger.addHandler(device_information_log_handler())
    logger.setLevel(logging.INFO)
    logger.info("Device information reading started.")

def load_cisco_switches():
    try:
        # Opening JSON file
        cisco_json_file = open(dir_path +'/cisco_xe_switches.json',) 
        # returns JSON object as a dictionary
        json_data = json.load(cisco_json_file)
        cisco_json_file.close()
        # maximum switches count to schedule
        max_count = 10
        json_directories = json_data['cisco_xe_switches']
        json_directory_count = len(json_directories)

        if json_directory_count > max_count:
            logger.warning("The maximum number(%s) of cisco devices that can be integrated to the schedule manager has been reached.", max_count)
            logger.info("Consider only %s cisco devices. Please contact system administrator to change the limit.", max_count)
            return json_directories[:max_count]
        else:
            logger.info("Schedule manager detected  %s number of cisco devices.", json_directory_count)
            return json_directories
    except Exception: 
                logging.exception("Error occurred while reading cisco device information json file.")
    finally:
            cisco_json_file.close()

def load_huawei_switches():
    try:
        # Opening JSON file
        huawei_json_file = open(dir_path +'/huawei_switches.json',) 
        # returns JSON object as a dictionary
        json_data = json.load(huawei_json_file)
        huawei_json_file.close()
        # maximum switches count to schedule
        max_count = 10
        json_directories = json_data['huawei_switches']
        json_directory_count = len(json_directories)

        if json_directory_count > max_count:
            logger.warning("The maximum number(%s) of huawei devices that can be integrated to the schedule manager has been reached.", max_count)
            logger.info("Consider only %s huawei devices. Please contact system administrator to change the limit.", max_count)
            return json_directories[:max_count]
        else:
            logger.info("Schedule manager detected  %s number of huawei devices.", json_directory_count)
            return json_directories
    except Exception: 
                logging.exception("Error occurred while reading huawei device information json file.")
    finally:
            huawei_json_file.close()