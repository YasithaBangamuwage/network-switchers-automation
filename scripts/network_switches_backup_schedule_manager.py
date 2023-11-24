from log_utils import *
from device_information_json_reader import (
    initialize_device_information_logger,
    load_cisco_switches,
    load_huawei_switches,
)
from cisco_backup_scheduler import initialize_cisco_backup_scheduler_logger
from cisco_backup_scheduler import generate_cisco_backups
from huawei_backup_scheduler import (
    generate_huawei_backups,
    initialize_huawei_backup_scheduler_logger,
)
from paramiko.ssh_exception import SSHException
import logging
import os
import datetime
import schedule
import time
import functools
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


# This decorator can be applied to any job function to log the elapsed time of each job
def print_elapsed_time(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start_timestamp = time.time()
        logger.info(
            'Network switches schedule manager: Running job - "%s"', func.__name__
        )
        result = func(*args, **kwargs)
        logger.info(
            'Network switches schedule manager: Job "%s" completed in %d seconds',
            func.__name__,
            (time.time() - start_timestamp),
        )
        next_backup_file_time_stamp = datetime.datetime.now() + timedelta(weeks=4)
        logger.info(
            'Backup Scheduler Next backup files "%s" will be created at: %s',
            func.__name__,
            next_backup_file_time_stamp.strftime("%Y_%m_%d-%I_%M_%S_%p"),
        )
        return result

    return wrapper


@print_elapsed_time
def trigger_cisco_backups():
    cisco_switches = load_cisco_switches()
    if len(cisco_switches) == 0:
        logger.error(
            "Could not able to found any cisco devices information to proceed the scheduler."
        )
        logger.error(
            "Please check the logs and correct device information then restart the windows service."
        )
    else:
        logger.info(
            "Network switches schedule manager start to process %s cisco devices. at: %s",
            len(cisco_switches),
            datetime.datetime.now().replace(microsecond=0),
        )
        generate_cisco_backups(cisco_switches)


@print_elapsed_time
def trigger_huawei_backups():
    huawei_switches = load_huawei_switches()
    if len(huawei_switches) == 0:
        logger.error(
            "Could not able to found any huawei devices information to proceed the scheduler."
        )
        logger.error(
            "Please check the logs and correct device information then restart the windows service."
        )
    else:
        logger.info(
            "Network switches schedule manager start to process %s huawei devices. at: %s",
            len(huawei_switches),
            datetime.datetime.now().replace(microsecond=0),
        )
        generate_huawei_backups(huawei_switches)


# initialize all logger files
initialize_root_logger()
create_main_backup_folder()
initialize_schedule_manager_logger()
initialize_device_information_logger()

# initialize cisco backup task
initialize_cisco_backup_scheduler_logger()
trigger_cisco_backups()
cisco_backup_scheduler = schedule.Scheduler()
cisco_backup_scheduler.every(10).seconds.do(trigger_cisco_backups)

# initialize huawei backup task
initialize_huawei_backup_scheduler_logger()
trigger_huawei_backups()
huawei_backup_scheduler = schedule.Scheduler()
huawei_backup_scheduler.every(10).seconds.do(trigger_huawei_backups)

while True:
    cisco_backup_scheduler.run_pending()
    huawei_backup_scheduler.run_pending()
    time.sleep(1)
