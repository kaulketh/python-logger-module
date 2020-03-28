import unittest

import logger


class LoggingTestCase(unittest.TestCase):
    from logger import LOGGER
    TEST_LOG_FOLDER = logger.logger.log_folder
    TEST_INFO_LOG = logger.logger.info_log_file
    TEST_ERROR_LOG = logger.logger.error_log_file

    def test1_logging(self):
        import logging
        self.result = False

        self.debug = "DEBUG" == logging.getLevelName(logging.DEBUG)
        self.info = "INFO" == logging.getLevelName(logging.INFO)
        self.warning = "WARNING" == logging.getLevelName(logging.WARNING)
        self.warn = "WARN" == logging.getLevelName(logging.WARN)
        self.error = "ERROR" == logging.getLevelName(logging.ERROR)
        # FATAL = CRITICAL, refer documentation
        self.fatal = "CRITICAL" == logging.getLevelName(logging.FATAL)
        self.critical = "CRITICAL" == logging.getLevelName(logging.CRITICAL)

        LoggingTestCase.LOGGER.debug(self.debug)
        LoggingTestCase.LOGGER.info(self.info)
        LoggingTestCase.LOGGER.warning(self.warning)
        # deprecated, refer documentation
        # LoggingTestCase.LOGGER.warn(self.warn)
        LoggingTestCase.LOGGER.error(self.error)
        LoggingTestCase.LOGGER.fatal(self.fatal)
        LoggingTestCase.LOGGER.critical(self.critical)

        self.result = \
            self.debug \
            and self.info \
            and self.warning \
            and self.error \
            and self.fatal \
            and self.critical

        if self.result:
            print("Logging OK")

        self.assertEqual(True, self.result, "Logging NOK!")

    def test2_file_creation(self):
        import os.path
        self.result = False
        self.folder = LoggingTestCase.TEST_LOG_FOLDER
        self.info_file = LoggingTestCase.TEST_INFO_LOG
        self.error_file = LoggingTestCase.TEST_ERROR_LOG

        self.result = os.path.isdir(self.folder)
        self.result = self.result and os.path.isfile(self.info_file)
        self.result = self.result and os.path.isfile(self.error_file)

        if self.result:
            print("Folder and file creation OK")

        self.assertEqual(True, self.result, "Folder and file creation NOK!")

    def test3_file_content(self):
        self.result = False
        self.folder = LoggingTestCase.TEST_LOG_FOLDER
        self.info = LoggingTestCase.TEST_INFO_LOG
        self.error = LoggingTestCase.TEST_ERROR_LOG
        self.search_info = "INFO"
        self.search_error = "ERROR"
        self.search_warn = "WARNING"
        self.search_critical = "CRITICAL"

        with open(self.info, 'r') as read_obj:
            for line in read_obj:
                if self.search_info in line:
                    self.result = self.search_info in line
                elif self.search_error in line:
                    self.result = self.result and self.search_error in line
                elif self.search_warn in line:
                    self.result = self.result and self.search_warn in line
                elif self.search_critical in line:
                    self.result = self.result and self.search_critical in line
                else:
                    self.result = False

        with open(self.error, 'r') as read_obj:
            for line in read_obj:
                if self.search_error in line:
                    self.result = self.result and self.search_error in line
                elif self.search_warn in line:
                    self.result = self.result and self.search_warn in line
                elif self.search_critical in line:
                    self.result = self.result and self.search_critical in line
                else:
                    self.result = False

        if self.result:
            print("File content check OK")

        self.assertEqual(True, self.result, "File content check NOK!")


if __name__ == '__main__':
    unittest.main()
