# utils/logger.py - Utility methods built from Python's logging library

import logging
import os
import sys
import traceback
from datetime import time

from scripts.housekeeping.datadir import get_log_dir


LOGGER_FORMAT = "%(name)s - %(levelname)s - %(filename)s / %(funcName)s / %(lineno)d - %(message)s"

LOGGER_LEVEL_DEFAULT = logging.ERROR
LOGGER_LEVEL_BETA = logging.DEBUG

logger = logging.


def logging_setup(default_logging_level: str):
    #
    _formatter = logging.Formatter(LOGGER_FORMAT)
    file_handler = _set_up_file_handler(_formatter)
    stream_handler = _set_up_stream_handler(_formatter)
    logging.root.addHandler(file_handler)
    logging.root.addHandler(stream_handler)

    prune_logs(logs_to_keep=10, retain_empty_logs=False)

    sys.excepthook = log_crash
    return


def _set_up_file_handler(formatter, level=LOGGER_LEVEL_DEFAULT) -> logging.FileHandler:
    # Logging for file
    timestr = time.strftime("%Y%m%d_%H%M%S")
    log_file_name = get_log_dir() + f"/clansim_{timestr}.log"
    file_handler = logging.FileHandler(log_file_name)
    file_handler.setFormatter(formatter)
    # Only log errors to file
    file_handler.setLevel(level)
    return file_handler

def _set_up_stream_handler(formatter, level=LOGGER_LEVEL_DEFAULT) -> logging.StreamHandler:
    # Logging for console
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)
    # Log debugging statements to console
    stream_handler.setLevel(level)
    return stream_handler


def prune_logs(logs_to_keep: int, retain_empty_logs: bool):
    log_files = os.listdir(get_log_dir())
    log_files.sort()
    log_files.reverse()

    log_list: dict[str] = {}

    for log_file in log_files:
        log_type = log_file.split('_')[0]

        if not log_list.__contains__(log_type):
            log_list[log_type] = 1
        else:
            if log_list[log_type] >= logs_to_keep or not retain_empty_logs and os.stat(f"{get_log_dir()}/{log_file}").st_size == 0:
                try:
                    os.remove(f"{get_log_dir()}/{log_file}")
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
