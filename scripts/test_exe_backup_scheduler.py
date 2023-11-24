import logging.handlers as handlers
from netmiko import ConnectHandler
from netmiko import NetMikoTimeoutException
from netmiko import NetMikoAuthenticationException
from paramiko.ssh_exception import SSHException
import logging
import os
import sys
import datetime
from dotenv import load_dotenv
import schedule
import time
from datetime import date, timedelta                    

exe_file = sys.executable
exe_parent = os.path.dirname(exe_file)
dotenv_path = os.path.join(exe_parent, ".env")
dir_path = os.path.dirname(exe_file)
logger = logging.getLogger()

def create_log_folder():
    if not os.path.exists(dir_path+ "/Logs"):
        os.makedirs(dir_path+ "/Logs")

def create_backup_folder():
    if not os.path.exists(dir_path+ "/Backups"):
        os.makedirs(dir_path+ "/Backups")
        logger.info("Backups directory created.")

def initialize_logger():
    create_log_folder()
    log_handler = handlers.RotatingFileHandler(dir_path+ '/Logs/logs.log', maxBytes=20000, backupCount=5)
    formatter = logging.Formatter('%(asctime)s %(levelname)s: %(message)s', "%Y-%m-%d %H:%M:%S")
    log_handler.setFormatter(formatter)
    logger.addHandler(log_handler)
    logger.setLevel(logging.INFO)
    logger.info("CISCO Backup Schedule Manager started.")
    
def load_env_variables():
    load_dotenv(dotenv_path=dotenv_path)
    global username
    username = os.environ.get('USER_NAME')
    global password
    password = os.environ.get('PASSWORD')
    global ip_address
    ip_address = os.environ.get('IP_ADDRESS')
    global device_type
    device_type = os.environ.get('DEVICE_TYPE')
    global secret
    secret = os.environ.get('SECRET')
    global is_all_env_values_provided
    is_all_env_values_provided = False

    if len(username.strip()) == 0:
        logger.warning("Please provide user name in environment file to connect the device. (Can not be empty)")
    elif len(password.strip()) == 0:
        logger.warning("Please provide password in environment file to connect the device. (Can not be empty)")
    elif  len(ip_address.strip()) == 0:
        logger.warning("Please provide ip address in environment file to connect the device. (Can not be empty)")
    elif  len(device_type.strip()) == 0:
        logger.warning("Please provide device type in environment file to connect the device. (Can not be empty)")
    elif  len(secret.strip()) == 0:
        logger.warning("Please provide secret in environment file to connect the device. (Can not be empty)")
    else:
        is_all_env_values_provided = True

def create_backup_file():
    time_now = datetime.datetime.now().replace(microsecond=0)
    if is_all_env_values_provided == False:
        logging.warning('Backup schedule task terminated due to incorrect device information.')
        logging.warning('Please update correct device information in env file and stop the process via Task Manager or windows service.')
        logging.warning('After updated please start windows service again.')
    else:
        DEVICE = {
                    'ip': ip_address,
                    'username': username,
                    'password': password,
                    'device_type': device_type,
  	                'secret': secret
                }
        try:
            #net_connect = ConnectHandler(**DEVICE)
            #net_connect.enable()
            #net_connect.find_prompt()
            logging.info('Device connected(IP address : %s) at %s', ip_address, str(time_now))
            #show_run_output = net_connect.send_command('show run')
            logging.info('Send commands to the connected device successfully.')
            #net_connect.disconnect()
            show_run_output ='temp output text data'# please remove this line
            backup_file_time_stamp = datetime.datetime.now().strftime("%Y_%m_%d-%I_%M_%S_%p")
            backup_file_name = 'SWITCH_' + ip_address + '-' + backup_file_time_stamp
            next_backup_file_time_stamp = datetime.datetime.now() + timedelta(weeks = 4) 

            try:
                filepath = os.path.join(dir_path + "/Backups", backup_file_name)
                backup_file = open(filepath + '.txt', 'w')
                backup_file.write(show_run_output)
                logging.info('Backup file created successfully. %s', backup_file_name)
                logging.info('Next backup file will be created at: %s', next_backup_file_time_stamp.strftime("%Y_%m_%d-%I_%M_%S_%p"))
            except Exception: 
                logging.exception("Error occurred while backup file creation")
            finally:
                backup_file.close()

        except NetMikoTimeoutException:
            logging.exception("Device not reachable (Please contact system administrator)")
        except NetMikoAuthenticationException:
            logging.exception('Authentication Failure (Please contact system administrator)')
        except SSHException:
            logging.exception('Make sure SSH is enabled (Please contact system administrator)')


#call configuration methods
initialize_logger()
create_backup_folder()
load_env_variables()
#trigger initial backup file
create_backup_file()

#call schedule task
schedule.every(10).seconds.do(create_backup_file)
#schedule.every(3).minutes.do(create_backup_file)
#schedule.every(4).weeks.do(create_backup_file)

while True:
    schedule.run_pending()
    time.sleep(1)