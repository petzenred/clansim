import logging
import os
import unittest
from copy import deepcopy
from unittest.mock import patch

from black import assert_equivalent

os.environ["SDL_VIDEODRIVER"] = "dummy"
os.environ["SDL_AUDIODRIVER"] = "dummy"

from utils import logger_utils

TEST_LOG_FILE_DIR = "./logs/"
TEST_LOG_FILE_NAME = f"test_logger_file_{logger_utils.TIMESTR_FORMAT}.log"
TEST_LOG_FILE_PATH = TEST_LOG_FILE_DIR + TEST_LOG_FILE_NAME


class TestLoggerUtils(unittest.TestCase):

    def test_logger_setup_debug(self):
        # test that logging at the DEBUG level works as expected
        test_text = "test_logger_setup_debug"
        logger_utils.logger_setup(_logging_level=logging.DEBUG,
                                  # TEST_LOG_FILE_DIR,
                                  _log_file_name=TEST_LOG_FILE_NAME)
        log = logging.getLogger("Test Logger - DEBUG")
        self.assertLogs(log, logging.DEBUG)
        self.assertNoLogs(log, logging.INFO)
        log.debug(test_text)
        log.info(test_text)
        # read logs to make sure each line was printed correctly
        with open(TEST_LOG_FILE_PATH, 'r') as fp:
            logs = fp.readlines()
            assert(len(logs)>=2)
            assert(test_text in logs[-2])
            assert(test_text in logs[-1])

    def test_logger_setup_info(self):
        # test that logging at the INFO level works as expected
        test_text = "test_logger_setup_info"
        logger_utils.logger_setup(logging.INFO,
                                  TEST_LOG_FILE_DIR,
                                  TEST_LOG_FILE_NAME)
        log = logging.getLogger("Test Logger - INFO")
        self.assertLogs(log, logging.INFO)
        self.assertNoLogs(log, logging.WARNING)
        log.debug(f"test_logger_setup_info")
        log.info(f"test_logger_setup_info")
        log.warning(f"test_logger_setup_info")
        # read logs to make sure each line was printed correctly
        with open(TEST_LOG_FILE_PATH, 'r') as fp:
            logs = fp.readlines()
            assert(len(logs)>=2)
            assert(test_text in logs[-2])
            assert(test_text in logs[-1])

    def test_logger_setup_warning(self):
        # test that logging at the WARNING level works as expected
        test_text = "test_logger_setup_warning"
        logger_utils.logger_setup(logging.WARNING,
                                  TEST_LOG_FILE_DIR,
                                  TEST_LOG_FILE_NAME)
        log = logging.getLogger("Test Logger - WARNING")
        self.assertLogs(log, logging.WARNING)
        self.assertNoLogs(log, logging.ERROR)
        log.debug(f"test_logger_setup_warning")
        log.warning(f"test_logger_setup_warning")
        log.error(f"test_logger_setup_warning")
        # read logs to make sure each line was printed correctly
        with open(TEST_LOG_FILE_PATH, 'r') as fp:
            logs = fp.readlines()
            assert(len(logs)>=2)
            assert(test_text in logs[-2])
            assert(test_text in logs[-1])

    def test_logger_setup_error(self):
        # test that logging at the ERROR level works as expected
        test_text = "test_logger_setup_error"
        logger_utils.logger_setup(logging.ERROR,
                                  TEST_LOG_FILE_DIR,
                                  TEST_LOG_FILE_NAME)
        log = logging.getLogger("Test Logger -DERROR")
        self.assertLogs(log, logging.ERROR)
        self.assertNoLogs(log, logging.CRITICAL)
        log.debug(f"test_logger_setup_error")
        log.error(f"test_logger_setup_error")
        log.critical(f"test_logger_setup_error")
        # read logs to make sure each line was printed correctly
        with open(TEST_LOG_FILE_PATH, 'r') as fp:
            logs = fp.readlines()
            assert(len(logs)>=2)
            assert(test_text in logs[-2])
            assert(test_text in logs[-1])

    def test_logger_setup_critical(self):
        # test that logging at the CRITICAL level works as expected
        test_text = "test_logger_setup_critical"
        logger_utils.logger_setup(logging.CRITICAL,
                                  TEST_LOG_FILE_DIR,
                                  TEST_LOG_FILE_NAME)
        log = logging.getLogger("Test Logger - CRITICAL")
        self.assertLogs(log, logging.CRITICAL)
        log.error(f"test_logger_setup_critical")
        log.critical(f"test_logger_setup_critical")
        # read logs to make sure each line was printed correctly
        with open(TEST_LOG_FILE_PATH, 'r') as fp:
            logs = fp.readlines()
            assert(len(logs)>=2)
            assert(test_text in logs[-2])
            assert(test_text in logs[-1])
