# utils/logger_utils.py - Utility methods built from Python's logging library

import logging
import os
import sys
import traceback
from datetime import time

from scripts.housekeeping.datadir import get_log_dir

LOGGER_FORMAT: str = "%(name)s - %(levelname)s - %(filename)s / %(funcName)s / %(lineno)d - %(message)s"
TIMESTR_FORMAT: str = "%Y%m%d_%H%M%S"
LOG_FILE_DIR = f"{get_log_dir()}/"
LOG_FILE_NAME = f"clansim_{TIMESTR_FORMAT}.log"

LOGGER_LEVEL_DEFAULT = logging.INFO
LOGGER_LEVEL_BETA = logging.DEBUG


def logger_setup(_logging_level=LOGGER_LEVEL_DEFAULT,
                 _log_file_dir=LOG_FILE_DIR,
                 _log_file_name=LOG_FILE_NAME):
    #
    _log_file_path = _log_file_dir + _log_file_name
    _formatter = logging.Formatter(LOGGER_FORMAT)
    logging.basicConfig(level=_logging_level,
                        format=LOGGER_FORMAT,
                        handlers=[
                            _set_up_file_handler(_formatter, _logging_level, _log_file_path),
                            _set_up_stream_handler(_formatter, _logging_level)
                        ])

    prune_logs(logs_to_keep=10, retain_empty_logs=False, log_file_dir=LOG_FILE_DIR)
    sys.excepthook = log_crash
    logging.debug("Logger setup complete")
    return


def _set_up_stream_handler(formatter, logging_level) -> logging.StreamHandler:
    # Logging for console
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)
    # Log debugging statements to console
    stream_handler.setLevel(logging_level)
    return stream_handler


def _set_up_file_handler(formatter, logging_level, log_file_path) -> logging.FileHandler:
    # Logging for file
    file_handler = logging.FileHandler(log_file_path)
    file_handler.setFormatter(formatter)
    file_handler.setLevel(logging_level)
    return file_handler


def prune_logs(logs_to_keep: int, retain_empty_logs: bool, log_file_dir=LOG_FILE_DIR):
    log_files = os.listdir(log_file_dir)
    log_files.sort()
    log_files.reverse()

    log_list: dict[str] = {}

    for log_file in log_files:
        log_type = log_file.split('_')[0]

        if not log_list.__contains__(log_type):
            log_list[log_type] = 1
        else:
            if log_list[log_type] >= logs_to_keep or not retain_empty_logs and os.stat(f"{log_file_dir}/{log_file}").st_size == 0:
                try:
                    os.remove(f"{log_file_dir}/{log_file}")
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
