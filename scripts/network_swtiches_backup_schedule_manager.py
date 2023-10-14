import logging.handlers as handlers
from log_utils import *
from device_information_json_reader import initialize_device_information_logger, load_cisco_switches, load_huawei_switches
from cisco_xe_backup_scheduler import initialize_cisco_xe_backup_scheduler_logger
from cisco_xe_backup_scheduler import generate_cisco_xe_backups
from netmiko import ConnectHandler
from netmiko import NetMikoTimeoutException
from netmiko import NetMikoAuthenticationException
from paramiko.ssh_exception import SSHException
import logging
import os
import sys
import datetime
import schedule
import time
from datetime import date, timedelta                    

exe_file = sys.executable
exe_parent = os.path.dirname(exe_file)
#dir_path = os.path.dirname(exe_file)
dir_path = os.path.dirname(os.path.realpath(__file__))
logger = logging.getLogger(__name__)


def create_main_backup_folder():
    if not os.path.exists(dir_path+ "/Backups"):
        os.makedirs(dir_path+ "/Backups")

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

# initialize all logger files
initialize_root_logger()
create_main_backup_folder()
initialize_schedule_manager_logger()
initialize_device_information_logger()

# initialize cisco_xe backup task
initialize_cisco_xe_backup_scheduler_logger()
trigger_cisco_xe_backups()
schedule.every(5).seconds.do(trigger_cisco_xe_backups)

while True:
    schedule.run_pending()
    time.sleep(1)