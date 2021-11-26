#!/usr/bin/python3
# -*- coding: utf-8 -*-
# -----------------------------------------------------------
# test.py
# created 26.11.2021
# Thomas Kaulke, kaulketh@gmail.com, thomas.kaulke@sumrise.io
# https://github.com/kaulketh
# -----------------------------------------------------------
import logging
import os
import sys
import unittest

from logger import PreconfiguredLogger

TEST_LOG = PreconfiguredLogger.instance

TEST_LOG_FOLDER = PreconfiguredLogger.LOG_FOLDER
TEST_INFO_LOG = PreconfiguredLogger.INF_LOG
TEST_ERROR_LOG = PreconfiguredLogger.ERR_LOG


class LoggingTestCase(unittest.TestCase):

    def test1_logging(self):
        self.result = True

        self.debug = "DEBUG" == logging.getLevelName(logging.DEBUG)
        self.info = "INFO" == logging.getLevelName(logging.INFO)
        self.warning = "WARNING" == logging.getLevelName(logging.WARNING)
        self.warn = "WARN" == logging.getLevelName(logging.WARN)
        self.error = "ERROR" == logging.getLevelName(logging.ERROR)
        # FATAL = CRITICAL, refer documentation
        self.fatal = "CRITICAL" == logging.getLevelName(logging.FATAL)
        self.critical = "CRITICAL" == logging.getLevelName(logging.CRITICAL)

        TEST_LOG.debug(self.debug)
        TEST_LOG.info(self.info)
        TEST_LOG.warning(self.warning)
        # deprecated, refer documentation
        # TEST_LOG.warn(self.warn)
        TEST_LOG.error(self.error)
        TEST_LOG.fatal(self.fatal)
        TEST_LOG.critical(self.critical)

        self.result &= \
            self.debug \
            and self.info \
            and self.warning \
            and self.error \
            and self.fatal \
            and self.critical

        if self.result:
            sys.stdout.write("Result: Logging OK\n")

        TEST_LOG.info("Success: " + str(self.result))

        self.assertEqual(True, self.result, "Logging NOK!")

    def test2_file_creation(self):
        self.result = True
        self.folder = TEST_LOG_FOLDER
        self.info_file = TEST_INFO_LOG
        self.error_file = TEST_ERROR_LOG

        self.result &= os.path.isdir(self.folder) \
                       and os.path.isfile(self.info_file) \
                       and os.path.isfile(self.error_file)

        if self.result:
            sys.stdout.write("Result: Folder and file creation OK\n")

        TEST_LOG.info("Success: " + str(self.result))

        self.assertEqual(True, self.result, "Folder and file creation NOK!")

    def test3_file_content(self):
        self.result = True
        self.folder = TEST_LOG_FOLDER
        self.info = TEST_INFO_LOG
        self.error = TEST_ERROR_LOG
        self.search_info = "INFO"
        self.search_error = "ERROR"
        self.search_warn = "WARNING"
        self.search_critical = "CRITICAL"

        with open(self.info, 'r') as read_obj:
            for line in read_obj:
                if self.search_info in line:
                    self.result &= self.search_info in line
                elif self.search_error in line:
                    self.result &= self.result and self.search_error in line
                elif self.search_warn in line:
                    self.result &= self.result and self.search_warn in line
                elif self.search_critical in line:
                    self.result &= self.result and self.search_critical in line
                else:
                    self.result &= False

        with open(self.error, 'r') as read_obj:
            for line in read_obj:
                if self.search_error in line:
                    self.result &= self.result and self.search_error in line
                elif self.search_warn in line:
                    self.result &= self.result and self.search_warn in line
                elif self.search_critical in line:
                    self.result &= self.result and self.search_critical in line
                else:
                    self.result &= False

        if self.result:
            sys.stdout.write("File content check OK\n")

        TEST_LOG.info("Success: " + str(self.result))

        self.assertEqual(True, self.result, "File content check NOK!")


def run(out=sys.stderr, verbosity=2):
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromModule(sys.modules[__name__])
    unittest.TextTestRunner(out, verbosity=verbosity).run(suite)


if __name__ == '__main__':
    with open('test.log', 'w') as f:
        run(out=f)
