import os
import sys


def get_directory_path():
    exe_file = sys.executable
    # dir_path = os.path.dirname(exe_file)
    dir_path = os.path.dirname(os.path.realpath(__file__))

    return dir_path
