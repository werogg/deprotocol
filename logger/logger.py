import logging


class Logger:
    _instance = None

    def __init__(self, name, level=logging.INFO, fmt='[%(asctime)s] %(levelname)s: %(message)s',
                 datefmt='%Y-%m-%d %H:%M:%S'):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(level)
        formatter = logging.Formatter(fmt=fmt, datefmt=datefmt)
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)

        # Check if the root logger already has a console handler
        root_logger = logging.getLogger('')
        if not root_logger.handlers:
            console_handler = logging.StreamHandler()
            console_handler.setFormatter(formatter)
            root_logger.addHandler(console_handler)

    def info(self, msg, *args, **kwargs):
        self.logger.info(msg, *args, **kwargs)

    def warning(self, msg, *args, **kwargs):
        self.logger.warning(msg, *args, **kwargs)

    def error(self, msg, *args, **kwargs):
        self.logger.error(msg, *args, **kwargs)

    @classmethod
    def get_instance(cls):
        if not cls._instance:
            cls._instance = cls('DeChat')
        return cls._instance

