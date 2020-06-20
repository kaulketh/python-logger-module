#!/usr/bin/python3
# -*- coding: utf-8 -*-

__author__ = "Thomas Kaulke"
__email__ = "kaulketh@gmail.com"

import errno
import logging
import os
from logging.config import fileConfig


class _Singleton(type):
    """ A metaclass that creates a Singleton base class when called.
        Works in Python 2 & 3
        https://www.it-swarm.dev/de/python/ein-singleton-python-erstellen/972393601
    """
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(_Singleton, cls).__call__(*args,
                                                                  **kwargs)
        return cls._instances[cls]


class Singleton(_Singleton('SingletonMeta', (object,), {})):
    """ Works in Python 2 & 3
        https://www.it-swarm.dev/de/python/ein-singleton-python-erstellen/972393601
    """
    pass


class PreconfLogger(Singleton):
    FOLDER = '../logs'
    # runtime location
    THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
    # define log folder related to location
    LOG_FOLDER = os.path.join(THIS_FOLDER, FOLDER)
    # define ini and log file pathes
    INI_FILE = 'debug.ini'
    INFO_LOG_FILE = LOG_FOLDER + '/info.log'
    ERROR_LOG_FILE = LOG_FOLDER + '/error.log'



    def __init__(self, name: str = __name__):
        self.this_folder = PreconfLogger.THIS_FOLDER
        self.log_folder = PreconfLogger.LOG_FOLDER
        self.ini_file = PreconfLogger.INI_FILE
        self.info_log_file = PreconfLogger.INFO_LOG_FILE
        self.error_log_file =PreconfLogger.ERROR_LOG_FILE

        # check if exists or create log folder
        try:
            os.makedirs(self.log_folder, exist_ok=True)  # Python > 3.2
        except TypeError:
            try:
                os.makedirs(self.log_folder)
            except OSError as exc:  # Python > 2.5
                if exc.errno == errno.EEXIST and os.path.isdir(
                        self.log_folder):
                    pass
                else:
                    raise

        # setup configuration
        self.config_file = os.path.join(self.this_folder, self.ini_file)
        fileConfig(self.config_file, disable_existing_loggers=True)

        # create handlers
        self.handler_info = logging.FileHandler(
            os.path.join(self.this_folder, self.info_log_file))
        self.handler_error = logging.FileHandler(
            os.path.join(self.this_folder, self.error_log_file))
        # set levels
        self.handler_info.setLevel(logging.INFO)
        self.handler_error.setLevel(logging.ERROR)

        # create formatters and add to handlers
        self.format_info = \
            logging.Formatter('%(asctime)s  %(levelname)s '
                              '[ %(module)s.%(funcName)s  linenr.%(lineno)s ] '
                              '%(message).180s', datefmt='%Y-%m-%d %H:%M:%S')
        self.format_error = \
            logging.Formatter(
                '%(asctime)s  %(levelname)s '
                '[ %(module)s.%(funcName)s  linenr.%(lineno)s ] '
                '[ thread: %(threadName)s ] %(message)s')
        self.handler_info.setFormatter(self.format_info)
        self.handler_error.setFormatter(self.format_error)

        # add handler
        self.logger = logging.getLogger(name)
        self.logger.addHandler(self.handler_info)
        self.logger.addHandler(self.handler_error)

    def get_instance(self):
        return self.logger


if __name__ == '__main__':
    pass
