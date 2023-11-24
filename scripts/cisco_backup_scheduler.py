from netmiko import ConnectHandler
from netmiko import NetMikoTimeoutException
from netmiko import NetMikoAuthenticationException
from paramiko.ssh_exception import SSHException
import logging
import os
import datetime
from datetime import date, timedelta                    
from log_utils import cisco_backup_scheduler_log_handler
from file_utils import get_directory_path

logger = logging.getLogger(__name__)

def initialize_cisco_backup_scheduler_logger():
    logger.addHandler(cisco_backup_scheduler_log_handler())
    logger.setLevel(logging.INFO)
    logger.info("CISCO Backup Scheduler started.")

def create_cisco_main_backup_folder():
    if not os.path.exists(get_directory_path() + "/Backups/cisco"):
        os.makedirs(get_directory_path() + "/Backups/cisco")
        logger.info("CISCO Backup Scheduler created main backup folder.")

def create_cisco_backup_folder(switch_folder_name):
    if not os.path.exists(get_directory_path() + "/Backups/cisco/" + switch_folder_name):
       os.makedirs(get_directory_path() + "/Backups/cisco/" + switch_folder_name)
       logger.info("CISCO Backup Scheduler created backup folder called : %s.", switch_folder_name)

def create_cisco_backup_file(switch_backup_folder_name, backup_file_name, backup_data):
    try:
        filepath = os.path.join(get_directory_path()  + "/Backups/cisco/" + switch_backup_folder_name, backup_file_name)
        backup_file = open(filepath + '.txt', 'w')
        backup_file.write(backup_data)
        logger.info('CISCO Backup Scheduler created backup file successfully. %s', backup_file_name)
        backup_file.close()
    except Exception: 
        logger.exception("CISCO Backup Scheduler error occurred while backup file creation")
    finally:
        backup_file.close()

def generate_cisco_backups(cisco_switches):
    #loop each switch and perform backup commands
    for cisco_switch in cisco_switches:
        #create backup folders
        create_cisco_main_backup_folder()
        switch_backup_folder_name = cisco_switch['tag_name'] + "_" + cisco_switch['ip_address']
        create_cisco_backup_folder(switch_backup_folder_name)
        time_now = datetime.datetime.now().replace(microsecond=0)
        #device configuration
        DEVICE = {
                    'ip': cisco_switch['ip_address'],
                    'username': cisco_switch['user_name'],
                    'password': cisco_switch['password'],
                    'device_type': cisco_switch['device_type'],
  	                'secret': cisco_switch['secret']
                }
        try:
            #net_connect = ConnectHandler(**DEVICE)
            #net_connect.enable()
            #net_connect.find_prompt()
            logger.info('CISCO Backup Scheduler connecting to (IP address : %s) at %s', cisco_switch['ip_address'], str(time_now))
            #show_run_output = net_connect.send_command('show run')
            show_run_output ='temp output text data'# please remove this line
            logger.info('CISCO Backup Scheduler connected to the device successfully.')
            #net_connect.disconnect()
            backup_file_time_stamp = datetime.datetime.now().strftime("%Y_%m_%d-%I_%M_%S_%p")
            backup_file_name = switch_backup_folder_name + '_' + backup_file_time_stamp
            create_cisco_backup_file(switch_backup_folder_name,backup_file_name, show_run_output)

        except NetMikoTimeoutException:
            logger.exception("Device not reachable (Please contact system administrator)")
        except NetMikoAuthenticationException:
            logger.exception('Authentication Failure (Please contact system administrator)')
        except SSHException:
            logger.exception('Make sure SSH is enabled (Please contact system administrator)')
