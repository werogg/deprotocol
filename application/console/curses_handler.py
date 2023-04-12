import logging


class CursesHandler(logging.Handler):
    def __init__(self, window):
        super().__init__()
        self.window = window

    def emit(self, record):
        try:
            msg = self.format(record)
            self.window.addstr(msg + '\n')
            self.window.refresh()
        except Exception:
            self.handleError(record)
