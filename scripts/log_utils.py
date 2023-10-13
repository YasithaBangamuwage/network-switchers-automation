import os
import logging
import logging.handlers as handlers
import sys
  
exe_file = sys.executable
exe_parent = os.path.dirname(exe_file)
dir_path = os.path.dirname(exe_file)
#dir_path = os.path.dirname(os.path.realpath(__file__))
logger = logging.getLogger()

def create_log_folder():
    if not os.path.exists(dir_path+ "/Logs"):
        os.makedirs(dir_path+ "/Logs")

def initialize_root_logger():
    create_log_folder()
    log_handler = handlers.RotatingFileHandler(dir_path+ '/Logs/server.log', maxBytes=20000, backupCount=5)
    formatter = logging.Formatter('%(asctime)s %(levelname)s: %(message)s', "%Y-%m-%d %H:%M:%S")
    log_handler.setFormatter(formatter)
    logger.addHandler(log_handler)
    logger.setLevel(logging.INFO)

def device_information_log_handler():
    log_handler = handlers.RotatingFileHandler(dir_path+ '/Logs/device_information_reader.log', maxBytes=20000, backupCount=5)
    formatter = logging.Formatter('%(asctime)s %(levelname)s: %(message)s', "%Y-%m-%d %H:%M:%S")
    log_handler.setFormatter(formatter)
    return log_handler

def schedule_manager_log_handler():
    log_handler = handlers.RotatingFileHandler(dir_path+ '/Logs/schedule_manager.log', maxBytes=20000, backupCount=5)
    formatter = logging.Formatter('%(asctime)s %(levelname)s: %(message)s', "%Y-%m-%d %H:%M:%S")
    log_handler.setFormatter(formatter)
    return log_handler