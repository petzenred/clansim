# logger_utils.py - Utility methods built from Python's logging library.

########################################################################################################################
# Imports
########################################################################################################################

import logging
import os
import sys
import traceback
from datetime import datetime
from pathlib import Path

from scripts.housekeeping.datadir import get_log_dir


########################################################################################################################
# Constants
########################################################################################################################

LOGGER_FORMAT: str = "%(name)s - %(levelname)s - %(filename)s / %(funcName)s / %(lineno)d - %(message)s"
TIMESTR_FORMAT: str = "%Y_%m_%d_%H_%M_%S"
LOG_FILE_DIR = get_log_dir()

# normal mode
LOGGER_LEVEL_DEFAULT = logging.INFO
DEFAULT_LOG_FILE_NAME: str = f"clansim_{TIMESTR_FORMAT}.log"

# debug mode
LOGGER_LEVEL_DEBUG = logging.DEBUG
DEBUG_LOG_FILE_NAME: str = f"debug_mode_clansim_{TIMESTR_FORMAT}.log"



########################################################################################################################
# Functions
########################################################################################################################

def logger_setup(debug_mode_f: bool = False,
                 _test_logging_info: tuple = None) -> Path:
    """ Set up the logger object, which will be used by the entire project.

    :param bool debug_mode_f: if True, logs are saved to the debug directory
    :param tuple _test_logging_info: only used for testing purposes, takes the form
            (_logging_level, _log_file_name)
    :return Path: path the log file is being saved to
    """
    # clean up old logs
    prune_logs(logs_to_keep=10, retain_empty_logs=False, log_file_dir=get_log_dir())

    # create logging config
    if _test_logging_info is not None:
        _logging_level = _test_logging_info[0]
        _log_file_name = _test_logging_info[1]
    elif debug_mode_f:
        _logging_level = LOGGER_LEVEL_DEBUG
        _log_file_name = DEBUG_LOG_FILE_NAME
    else:
        _logging_level = LOGGER_LEVEL_DEFAULT
        _log_file_name = DEFAULT_LOG_FILE_NAME

    _log_file_name = datetime.now().strftime(_log_file_name)
    _log_file_path = Path(get_log_dir(), _log_file_name)
    _formatter = logging.Formatter(LOGGER_FORMAT)
    logging.basicConfig(level=_logging_level,
                        format=LOGGER_FORMAT,
                        handlers=[
                            _set_up_file_handler(_formatter, _logging_level, _log_file_path),
                            _set_up_stream_handler(_formatter, _logging_level)
                            ],
                        force=True)

    sys.excepthook = log_crash
    return _log_file_path


def _set_up_file_handler(formatter, logging_level, log_file_path) -> logging.FileHandler:
    # Logging for file
    file_handler = logging.FileHandler(log_file_path)
    file_handler.setFormatter(formatter)
    file_handler.setLevel(logging_level)
    return file_handler


def _set_up_stream_handler(formatter, logging_level) -> logging.StreamHandler:
    # Logging for console
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)
    # Log debugging statements to console
    stream_handler.setLevel(logging_level)
    return stream_handler


def prune_logs(logs_to_keep: int, retain_empty_logs: bool, log_file_dir=LOG_FILE_DIR):
    log_files = os.listdir(log_file_dir)
    log_files.sort()
    log_files.reverse()

    log_list: dict = {}

    for log_file in log_files:
        log_type = str(log_file).split('_')[0]

        if not log_list.__contains__(log_type):
            log_list[log_type] = 1
        else:
            log_path: Path = Path(log_file_dir, log_file)
            if (log_list[log_type] >= logs_to_keep
                    or not retain_empty_logs
                    and os.stat(log_path).st_size == 0):
                try:
                    os.remove(log_path)
                except PermissionError:
                    traceback.print_exc()
            else:
                log_list[log_type] += 1


def log_crash(logtype, value, tb):
    """
    Log uncaught exceptions to file
    """
    logging.critical("Uncaught exception", exc_info=(logtype, value, tb))
    sys.__excepthook__(type, value, tb)
