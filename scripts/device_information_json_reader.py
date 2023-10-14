import json
import logging
from log_utils import device_information_log_handler
from jsonschema import validate, ValidationError, SchemaError
from file_utils import get_directory_path

logger = logging.getLogger(__name__)

def initialize_device_information_logger():
    logger.addHandler(device_information_log_handler())
    logger.setLevel(logging.INFO)
    logger.info("Device information reading started.")

def load_cisco_switches():
    try:
        # Opening JSON file
        cisco_json_file = open(get_directory_path() +'/cisco_xe_switches.json',) 
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
            is_valid = validate_cisco_xe_json_schema(json_directories)
            if is_valid:
                 return json_directories[:max_count]
            else:
                 return []
        else:
            logger.info("Schedule manager detected  %s number of cisco devices.", json_directory_count)
            is_valid = validate_cisco_xe_json_schema(json_directories)
            if is_valid:
                 return json_directories
            else:
                 return []
    except Exception: 
                logger.exception("Error occurred while reading cisco device information json file.")
    finally:
            cisco_json_file.close()

def load_huawei_switches():
    try:
        # Opening JSON file
        huawei_json_file = open(get_directory_path()  +'/huawei_switches.json',) 
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
            is_valid = validate_huawei_json_schema(json_directories)
            if is_valid:
                 return json_directories[:max_count]
            else:
                 return []
        else:
            logger.info("Schedule manager detected  %s number of huawei devices.", json_directory_count)
            is_valid = validate_huawei_json_schema(json_directories)
            if is_valid:
                 return json_directories
            else:
                 return []
    except Exception: 
                logging.exception("Error occurred while reading huawei device information json file.")
    finally:
            huawei_json_file.close()

def validate_cisco_xe_json_schema(directories):
    schema_validator = {
    "type"  :   "object",
    "properties"    :{
                    "tag_name" : {"type" : "string", "minLength": 1},
                    "user_name" :{"type" : "string", "minLength": 1},
                    "password" :{"type" : "string", "minLength": 1},
                    "ip_address" :{"type" : "string", "minLength": 1},
                    "device_type" :{"type" : "string", "minLength": 1},
                    "secret" :{"type" : "string", "minLength": 1},
                    },
    "required":     ["tag_name", "user_name", "password", "ip_address", "device_type", "secret"]
    }

    try:
        for directory in directories:
            validate(directory, schema_validator)
        return True
 
    except SchemaError as e:
        logger.error("Error occurred while reading cisco_xe device information json file. Wrong json schema")
        logger.error("All cisco_xe device information reading ignored and please correct it and restart the service to proceed with cisco_xe devices.")
        logger.exception("Error occurred while reading cisco_xe device information json file.")
        return False
     
    except ValidationError as e:
        logger.error("Error occurred while reading cisco_xe device information json file. Wrong json schema")
        logger.error("All cisco_xe device information reading ignored and please correct it and restart the service to proceed with cisco_xe devices.")
        logger.exception("Error occurred while reading cisco_xe device information json file.")
        return False
    
def validate_huawei_json_schema(directories):
    schema_validator = {
    "type"  :   "object",
    "properties"    :{
                    "tag_name" : {"type" : "string", "minLength": 1},
                    "user_name" :{"type" : "string", "minLength": 1},
                    "password" :{"type" : "string", "minLength": 1},
                    "ip_address" :{"type" : "string", "minLength": 1},
                    "device_type" :{"type" : "string", "minLength": 1},
                    "secret" :{"type" : "string", "minLength": 1},
                    },
    "required":     ["tag_name", "user_name", "password", "ip_address", "device_type", "secret"]
    }

    try:
        for directory in directories:
            validate(directory, schema_validator)
        return True
 
    except SchemaError as e:
        logger.error("Error occurred while reading huawei device information json file. Wrong json schema")
        logger.error("All huawei device information reading ignored and please correct it and restart the service to proceed with huawei devices.")
        logger.exception("Error occurred while reading huawei device information json file.")
        return False
     
    except ValidationError as e:
        logger.error("Error occurred while reading huawei device information json file. Wrong json schema")
        logger.error("All huawei device information reading ignored and please correct it and restart the service to proceed with huawei devices.")
        logger.exception("Error occurred while reading huawei device information json file.")
        return False