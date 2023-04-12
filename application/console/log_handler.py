import logging

class QueueHandler(logging.Handler):

    def __init__(self, log_queue):

        super().__init__()
        self.log_queue = log_queue

    def emit(self, record):
        self.log_queue.put(record)