import logging.handlers as handlers
from log_utils import *
from device_information_json_reader import initialize_device_information_logger, load_cisco_switches, load_huawei_switches

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
dir_path = os.path.dirname(exe_file)
#dir_path = os.path.dirname(os.path.realpath(__file__))
logger = logging.getLogger(__name__)


def create_backup_folder():
    if not os.path.exists(dir_path+ "/Backups"):
        os.makedirs(dir_path+ "/Backups")

def initialize_schedule_manager_logger():
    logger.addHandler(schedule_manager_log_handler())
    logger.setLevel(logging.INFO)
    logger.info("Network switches schedule manager started.")


initialize_root_logger()
create_backup_folder()
initialize_schedule_manager_logger()
initialize_device_information_logger()
cisco_switches = load_cisco_switches()
huawei_switches = load_huawei_switches()
print(cisco_switches)
print(huawei_switches)
