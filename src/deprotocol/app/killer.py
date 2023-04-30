import signal


class GracefulKiller:
    kill_now = False

    def __init__(self, deprotocol):
        signal.signal(signal.SIGINT, self.exit_gracefully)
        signal.signal(signal.SIGTERM, self.exit_gracefully)
        self.deprotocol = deprotocol

    def exit_gracefully(self, *args):
        self.kill_now = True
        self.deprotocol.on_stop()
