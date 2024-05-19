"""
Util functions for mtg_deckbuilding
"""
import os
from pathlib import Path


def file_exists(file_name):
    """Uses a filepath + filenam string and determines if the file exists"""
    if os.path.exists(file_name):
        return True
    return False


def get_cache_directory():
    """Returns the string of the XDG cache directory .cache, useful to append to the home directory, 
    getHomeDirectory, to construct the path of the current users cache directory"""
    return ".cache/"


def get_home_directory():
    """Returns a string of the current home directory"""
    return str(Path.home())
