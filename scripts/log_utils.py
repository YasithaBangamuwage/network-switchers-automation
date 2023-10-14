import os
import logging
import logging.handlers as handlers
import sys
from file_utils import get_directory_path

logger = logging.getLogger()

def create_log_folder():
    if not os.path.exists(get_directory_path() + "/Logs"):
        os.makedirs(get_directory_path() + "/Logs")

def initialize_root_logger():
    create_log_folder()
    log_handler = handlers.RotatingFileHandler(get_directory_path()  + '/Logs/server.log', maxBytes=200000, backupCount=5)
    formatter = logging.Formatter('%(asctime)s %(levelname)s: %(message)s', "%Y-%m-%d %H:%M:%S")
    log_handler.setFormatter(formatter)
    logger.addHandler(log_handler)
    logger.setLevel(logging.INFO)

def device_information_log_handler():
    log_handler = handlers.RotatingFileHandler(get_directory_path()  + '/Logs/device_information_reader.log', maxBytes=200000, backupCount=5)
    formatter = logging.Formatter('%(asctime)s %(levelname)s: %(message)s', "%Y-%m-%d %H:%M:%S")
    log_handler.setFormatter(formatter)
    return log_handler

def schedule_manager_log_handler():
    log_handler = handlers.RotatingFileHandler(get_directory_path()  + '/Logs/schedule_manager.log', maxBytes=200000, backupCount=5)
    formatter = logging.Formatter('%(asctime)s %(levelname)s: %(message)s', "%Y-%m-%d %H:%M:%S")
    log_handler.setFormatter(formatter)
    return log_handler

def cisco_xe_backup_scheduler_log_handler():
    log_handler = handlers.RotatingFileHandler(get_directory_path()  + '/Logs/cisco_xe_backup_scheduler.log', maxBytes=200000, backupCount=5)
    formatter = logging.Formatter('%(asctime)s %(levelname)s: %(message)s', "%Y-%m-%d %H:%M:%S")
    log_handler.setFormatter(formatter)
    return log_handler

def huawei_backup_scheduler_log_handler():
    log_handler = handlers.RotatingFileHandler(get_directory_path()  + '/Logs/huawei_backup_scheduler.log', maxBytes=200000, backupCount=5)
    formatter = logging.Formatter('%(asctime)s %(levelname)s: %(message)s', "%Y-%m-%d %H:%M:%S")
    log_handler.setFormatter(formatter)
    return log_handler