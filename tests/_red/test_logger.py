import logging
import os
import unittest

os.environ["SDL_VIDEODRIVER"] = "dummy"
os.environ["SDL_AUDIODRIVER"] = "dummy"

from scripts._red.utils import logger_utils

TEST_LOG_TEXT_DEBUG = "This was written at level DEBUG."
TEST_LOG_TEXT_INFO = "This was written at level INFO."
TEST_LOG_TEXT_WARNING = "This was written at level WARNING."
TEST_LOG_TEXT_ERROR = "This was written at level ERROR."
TEST_LOG_TEXT_CRITICAL = "This was written at level CRITICAL."
TEST_LOG_TEXT = [
    TEST_LOG_TEXT_DEBUG,
    TEST_LOG_TEXT_INFO,
    TEST_LOG_TEXT_WARNING,
    TEST_LOG_TEXT_ERROR,
    TEST_LOG_TEXT_CRITICAL,
]


class TestLoggerUtils(unittest.TestCase):

    def test_logger_setup_debug_flag_false(self):
        log_path = logger_utils.logger_setup(debug_mode_f=False)
        logger = logging.getLogger("Test_Logger_Debug_Flag_False")

        try:
            # write to logger at all levels
            self.assertLogs(logger, logging.DEBUG)
            logger.debug(TEST_LOG_TEXT_DEBUG)
            self.assertLogs(logger, logging.INFO)
            logger.info(TEST_LOG_TEXT_INFO)
            self.assertLogs(logger, logging.WARNING)
            logger.warning(TEST_LOG_TEXT_WARNING)
            self.assertLogs(logger, logging.ERROR)
            logger.error(TEST_LOG_TEXT_ERROR)
            self.assertLogs(logger, logging.CRITICAL)
            logger.critical(TEST_LOG_TEXT_CRITICAL)

            # read log file to make sure each line was printed correctly
            with open(log_path, 'r') as fp:
                logs = fp.readlines()
                assert(len(logs)==4)
                for no, line in enumerate(logs):
                    assert(TEST_LOG_TEXT[1:][no] in line)
        finally:
            os.remove(log_path)

    def test_logger_setup_debug_flag_true(self):
        log_path = logger_utils.logger_setup(debug_mode_f=True)
        logger = logging.getLogger("Test_Logger_Debug_Flag_True")

        try:
            # write to logger at all levels
            self.assertLogs(logger, logging.DEBUG)
            logger.debug(TEST_LOG_TEXT_DEBUG)
            self.assertLogs(logger, logging.INFO)
            logger.info(TEST_LOG_TEXT_INFO)
            self.assertLogs(logger, logging.WARNING)
            logger.warning(TEST_LOG_TEXT_WARNING)
            self.assertLogs(logger, logging.ERROR)
            logger.error(TEST_LOG_TEXT_ERROR)
            self.assertLogs(logger, logging.CRITICAL)
            logger.critical(TEST_LOG_TEXT_CRITICAL)

            # read log file to make sure each line was printed correctly
            with open(log_path, 'r') as fp:
                logs = fp.readlines()
                assert(len(logs)==5)
                for no, line in enumerate(logs):
                    assert(TEST_LOG_TEXT[no] in line)
        finally:
            os.remove(log_path)

    def test_logger_write_debug(self):
        # set up the logger
        log_file = f"test/test_log_debug_{logger_utils.TIMESTR_FORMAT}.log"
        test_logging_info = (logging.DEBUG, log_file)
        log_path = logger_utils.logger_setup(_test_logging_info=test_logging_info)
        logger = logging.getLogger("Test_Logger_Debug")

        try:
            # write to logger at all levels
            self.assertLogs(logger, logging.DEBUG)
            logger.debug(TEST_LOG_TEXT_DEBUG)
            self.assertLogs(logger, logging.INFO)
            logger.info(TEST_LOG_TEXT_INFO)
            self.assertLogs(logger, logging.WARNING)
            logger.warning(TEST_LOG_TEXT_WARNING)
            self.assertLogs(logger, logging.ERROR)
            logger.error(TEST_LOG_TEXT_ERROR)
            self.assertLogs(logger, logging.CRITICAL)
            logger.critical(TEST_LOG_TEXT_CRITICAL)

            # read log file to make sure each line was printed correctly
            with open(log_path, 'r') as fp:
                logs = fp.readlines()
                assert(len(logs)==5)
                for no, line in enumerate(logs):
                    assert(TEST_LOG_TEXT[no] in line)
        finally:
            os.remove(log_path)

    def test_logger_write_info(self):
        # set up the logger
        log_file = f"test/test_log_info_{logger_utils.TIMESTR_FORMAT}.log"
        test_logging_info = (logging.INFO, log_file)
        log_path = logger_utils.logger_setup(_test_logging_info=test_logging_info)
        logger = logging.getLogger("Test_Logger_Info")

        try:
            # write to logger at all levels
            self.assertNoLogs(logger, logging.DEBUG)
            logger.debug(TEST_LOG_TEXT_DEBUG)
            self.assertLogs(logger, logging.INFO)
            logger.info(TEST_LOG_TEXT_INFO)
            self.assertLogs(logger, logging.WARNING)
            logger.warning(TEST_LOG_TEXT_WARNING)
            self.assertLogs(logger, logging.ERROR)
            logger.error(TEST_LOG_TEXT_ERROR)
            self.assertLogs(logger, logging.CRITICAL)
            logger.critical(TEST_LOG_TEXT_CRITICAL)

            # read log file to make sure each line was printed correctly
            with open(log_path, 'r') as fp:
                logs = fp.readlines()
                assert(len(logs)==4)
                for no, line in enumerate(logs):
                    assert(TEST_LOG_TEXT[1:][no] in line)
        finally:
            os.remove(log_path)

    def test_logger_write_warning(self):
        # set up the logger
        log_file = f"test/test_log_warning_{logger_utils.TIMESTR_FORMAT}.log"
        test_logging_info = (logging.WARNING, log_file)
        log_path = logger_utils.logger_setup(_test_logging_info=test_logging_info)
        logger = logging.getLogger("Test_Logger_Warning")

        try:
            # write to logger at all levels
            self.assertNoLogs(logger, logging.DEBUG)
            logger.debug(TEST_LOG_TEXT_DEBUG)
            self.assertNoLogs(logger, logging.INFO)
            logger.info(TEST_LOG_TEXT_INFO)
            self.assertLogs(logger, logging.WARNING)
            logger.warning(TEST_LOG_TEXT_WARNING)
            self.assertLogs(logger, logging.ERROR)
            logger.error(TEST_LOG_TEXT_ERROR)
            self.assertLogs(logger, logging.CRITICAL)
            logger.critical(TEST_LOG_TEXT_CRITICAL)

            # read log file to make sure each line was printed correctly
            with open(log_path, 'r') as fp:
                logs = fp.readlines()
                assert(len(logs)==3)
                for no, line in enumerate(logs):
                    assert(TEST_LOG_TEXT[2:][no] in line)
        finally:
            os.remove(log_path)

    def test_logger_write_error(self):
        # set up the logger
        log_file = f"test/test_log_error_{logger_utils.TIMESTR_FORMAT}.log"
        test_logging_info = (logging.ERROR, log_file)
        log_path = logger_utils.logger_setup(_test_logging_info=test_logging_info)
        logger = logging.getLogger("Test_Logger_Error")

        try:
            # write to logger at all levels
            self.assertNoLogs(logger, logging.DEBUG)
            logger.debug(TEST_LOG_TEXT_DEBUG)
            self.assertNoLogs(logger, logging.INFO)
            logger.info(TEST_LOG_TEXT_INFO)
            self.assertNoLogs(logger, logging.WARNING)
            logger.warning(TEST_LOG_TEXT_WARNING)
            self.assertLogs(logger, logging.ERROR)
            logger.error(TEST_LOG_TEXT_ERROR)
            self.assertLogs(logger, logging.CRITICAL)
            logger.critical(TEST_LOG_TEXT_CRITICAL)

            # read log file to make sure each line was printed correctly
            with open(log_path, 'r') as fp:
                logs = fp.readlines()
                assert(len(logs)==2)
                for no, line in enumerate(logs):
                    assert(TEST_LOG_TEXT[3:][no] in line)
        finally:
            os.remove(log_path)

    def test_logger_write_critical(self):
        # set up the logger
        log_file = f"test/test_log_critical_{logger_utils.TIMESTR_FORMAT}.log"
        test_logging_info = (logging.CRITICAL, log_file)
        log_path = logger_utils.logger_setup(_test_logging_info=test_logging_info)
        logger = logging.getLogger("Test_Logger_Critical")

        try:
            # write to logger at all levels
            self.assertNoLogs(logger, logging.DEBUG)
            logger.debug(TEST_LOG_TEXT_DEBUG)
            self.assertNoLogs(logger, logging.INFO)
            logger.info(TEST_LOG_TEXT_INFO)
            self.assertNoLogs(logger, logging.WARNING)
            logger.warning(TEST_LOG_TEXT_WARNING)
            self.assertNoLogs(logger, logging.ERROR)
            logger.error(TEST_LOG_TEXT_ERROR)
            self.assertLogs(logger, logging.CRITICAL)
            logger.critical(TEST_LOG_TEXT_CRITICAL)

            # read log file to make sure each line was printed correctly
            with open(log_path, 'r') as fp:
                logs = fp.readlines()
                assert(len(logs)==1)
                for no, line in enumerate(logs):
                    assert(TEST_LOG_TEXT[4:][no] in line)
        finally:
            os.remove(log_path)
