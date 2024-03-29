import threading
import time

from deprotocol.app.logger import Logger
from deprotocol.network.protocol.packets.keepalive import KeepAlivePacket


class Pinger(threading.Thread):
    def __init__(self, node_connection):
        super(Pinger, self).__init__()
        self.terminate_flag = threading.Event()
        self.last_ping = time.time()
        self.node_connection = node_connection
        self.dead_time = 120  # time to disconnect from node if not pinged
        self.send_time = 10

    def stop(self):
        self.terminate_flag.set()
        Logger.get_logger().trace('pinger_stop: terminate_flag set')

    def run(self):
        Logger.get_logger().info("Pinger Started")
        time.sleep(1)
        while not self.terminate_flag.is_set():
            ping_packet = KeepAlivePacket()
            try:
                self.node_connection.packet_handler.send_packet(ping_packet)
            except Exception as exc:
                Logger.get_logger().error(exc)
            Logger.get_logger().trace(f'pinger_run: Ping packet sent, sleeping {self.send_time} seconds...')
            time.sleep(self.send_time)

        Logger.get_logger().info("Pinger stopped")
