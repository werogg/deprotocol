""" Module providing logger class to handle multiple logging functionalities in singleton"""
import logging
from stem.util import log as stem_log


class Logger:
    """ Represents a Logger object handles logging functionalities executed as a singleton"""
    _instance = None

    def __init__(self, name, level=logging.INFO, fmt='[%(asctime)s] %(levelname)s: %(message)s',
                 datefmt='%Y-%m-%d %H:%M:%S'):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(level)
        formatter = logging.Formatter(fmt=fmt, datefmt=datefmt)

        # Check if the root logger already has a console handler
        root_logger = logging.getLogger('')
        if not root_logger.handlers:
            console_handler = logging.StreamHandler()
            console_handler.setFormatter(formatter)
            root_logger.addHandler(console_handler)

        #stem_logger = stem_log.get_logger()
        #stem_logger.propagate = False

        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)

        #stem_logger.addHandler(logging.StreamHandler())

    def level(self, level="trace"):
        self.logger.setLevel(level)

    def info(self, msg, *args, **kwargs):
        """ Information prints in logging terms """
        self.logger.info(msg, *args, **kwargs)

    def warning(self, msg, *args, **kwargs):
        """ Warning prints in logging terms """
        self.logger.warning(msg, *args, **kwargs)

    def error(self, msg, *args, **kwargs):
        """ Error prints in logging terms"""
        self.logger.error(msg, *args, **kwargs)

    def debug(self, msg, *args, **kwargs):
        """ Debug prints in logging terms """
        self.logger.debug(msg, *args, **kwargs)

    @classmethod
    def get_instance(cls):
        """ Singleton method to get the Logger instance """
        if not cls._instance:
            cls._instance = cls('DeChat')
        return cls._instance
