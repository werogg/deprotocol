""" Module providing logger class to handle multiple logging functionalities in singleton"""
import datetime
import logging
import os

from charset_normalizer.constant import TRACE

from deprotocol.settings import APP_NAME
from deprotocol.settings import LOG_LEVEL


class Logger:
    """ Represents a Logger object handles logging functionalities executed as a singleton"""
    _instance = None

    def __init__(self, name, level=LOG_LEVEL, fmt='[%(asctime)s] %(levelname)s: %(message)s',
                 datefmt='%Y-%m-%d %H:%M:%S'):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(level)

        if not os.path.exists('logs'):
            os.makedirs('logs')

        logging.addLevelName(TRACE, 'TRACE')
        setattr(self.logger, 'trace', lambda message, *args: self.logger.log(TRACE, message, *args))

        console_handler = logging.StreamHandler()
        console_handler.setLevel(level)

        formatter = logging.Formatter(fmt=fmt, datefmt=datefmt)
        console_handler.setFormatter(formatter)
        self.logger.addHandler(console_handler)

        timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
        file_handler = logging.FileHandler(f'logs/{name}_{timestamp}.log')
        file_handler.setFormatter(formatter)
        self.logger.addHandler(file_handler)

    @classmethod
    def get_logger(cls):
        """ Singleton method to get the Logger instance """
        if not cls._instance:
            cls._instance = cls(name=APP_NAME, level=LOG_LEVEL)
        return cls._instance.logger
