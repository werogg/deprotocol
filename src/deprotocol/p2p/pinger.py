import threading
import time

from deprotocol.logger.logger import Logger


class Pinger(threading.Thread):
    def __init__(self, parent):
        self.terminate_flag = threading.Event()
        super(Pinger, self).__init__()  # CAll Thread.__init__()
        self.parent = parent
        self.dead_time = 30  # time to disconect from node if not pinged

    def stop(self):
        self.terminate_flag.set()
        Logger.get_logger().trace('pinger_stop: terminate_flag set')

    def run(self):
        Logger.get_logger().info("Pinger Started")
        while (
                not self.terminate_flag.is_set()
        ):  # Check whether the thread needs to be closed
            for i in self.parent.node_connections:
                i.send("ping")
                Logger.get_logger().trace('pinger_run: Ping packet sent, sleeping 20 seconds...')
                time.sleep(20)
        Logger.get_logger().info("Pinger stopped")
