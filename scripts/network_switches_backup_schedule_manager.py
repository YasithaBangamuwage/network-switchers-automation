from log_utils import *
from device_information_json_reader import initialize_device_information_logger, load_cisco_switches, load_huawei_switches
from cisco_xe_backup_scheduler import initialize_cisco_xe_backup_scheduler_logger
from cisco_xe_backup_scheduler import generate_cisco_xe_backups
from huawei_backup_scheduler import generate_huawei_backups, initialize_huawei_backup_scheduler_logger
from paramiko.ssh_exception import SSHException
import logging
import os
import datetime
import schedule
import time
from datetime import date, timedelta                    
from file_utils import get_directory_path

logger = logging.getLogger(__name__)


def create_main_backup_folder():
    if not os.path.exists(get_directory_path() + "/Backups"):
        os.makedirs(get_directory_path() + "/Backups")

def initialize_schedule_manager_logger():
    logger.addHandler(schedule_manager_log_handler())
    logger.setLevel(logging.INFO)
    logger.info("Network switches schedule manager started.")

def trigger_cisco_xe_backups():
    cisco_switches = load_cisco_switches()
    if len(cisco_switches) == 0:
        logger.error("Could not able to found any cisco devices information to proceed the scheduler.")
        logger.error("Please check the logs and correct device information then restart the windows service.")
    else:
        logger.info("Network switches schedule manager start to process %s cisco_xe devices. at: %s", len(cisco_switches), datetime.datetime.now().replace(microsecond=0))
        generate_cisco_xe_backups(cisco_switches)

def trigger_huawei_backups():
    huawei_switches = load_huawei_switches()
    if len(huawei_switches) == 0:
        logger.error("Could not able to found any huawei devices information to proceed the scheduler.")
        logger.error("Please check the logs and correct device information then restart the windows service.")
    else:
        logger.info("Network switches schedule manager start to process %s huawei devices. at: %s", len(huawei_switches), datetime.datetime.now().replace(microsecond=0))
        generate_huawei_backups(huawei_switches)

# initialize all logger files
initialize_root_logger()
create_main_backup_folder()
initialize_schedule_manager_logger()
initialize_device_information_logger()

# initialize cisco_xe backup task
initialize_cisco_xe_backup_scheduler_logger()
trigger_cisco_xe_backups()
schedule.every(10).seconds.do(trigger_cisco_xe_backups)

# initialize huawei backup task
initialize_huawei_backup_scheduler_logger()
trigger_huawei_backups()
schedule.every(10).seconds.do(trigger_huawei_backups)

while True:
    schedule.run_pending()
    time.sleep(1)