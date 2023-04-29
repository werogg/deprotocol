import socket
import sys
import threading
import time

import socks
import stem

from deprotocol.logger.logger import Logger
from deprotocol.p2p.pinger import Pinger
from deprotocol.protocol.packet_handler import PacketHandler
from deprotocol.protocol.type import PacketType


class NodeConnection(threading.Thread):
    def __init__(self, sock):
        super(NodeConnection, self).__init__()
        socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5, '127.0.0.1', 9050)
        self.sock = sock
        self.pinger = None
        self.packet_handler = PacketHandler(sock)
        self.terminate_flag = threading.Event()

    def start(self):
        self.pinger = Pinger(self)
        self.pinger.start()

    def send_packet(self, packet):
        self.packet_handler.send_packet(packet)

    def stop(self):
        self.terminate_flag.set()

    def run(self):
        self.sock.settimeout(60.0)

        while not self.terminate_flag.is_set():
            if time.time() - self.pinger.last_ping > self.pinger.dead_time:
                self.terminate_flag.set()
                Logger.get_logger().warning("Node died")

            try:
                received_packet = self.packet_handler.receive_packet()
                if received_packet.TYPE == PacketType.KEEP_ALIVE:
                    self.pinger.last_ping = time.time()
            except socket.timeout:
                Logger.get_logger().error("NodeConnection: timeout")
            except Exception as e:
                self.terminate_flag.set()
                Logger.get_logger().error("NodeConnection: Socket has been terminated")
                Logger.get_logger().error(e)




