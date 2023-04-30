import json
import socket
import threading
import time

import socks

from deprotocol.app.user import User
from deprotocol.event.events.packet_received_event import PacketReceivedEvent
from deprotocol.app.logger import Logger
from deprotocol.network.peer_networking.handler.received_packet_handler import ReceivedPacketHandler
from deprotocol.network.peer_networking.pinger import Pinger
from deprotocol.network.protocol.packet_factory import PacketFactory
from deprotocol.network.protocol.packet_handler import PacketHandler
from deprotocol.network.protocol.payloads.handshake_payload import HandshakePayload
from deprotocol.network.protocol.type import PacketType
from deprotocol.utils import crypto_funcs as cf


class NodeConnection(threading.Thread):
    def __init__(self, deprotocol, sock, id):
        super().__init__()
        self.id = id
        self.deprotocol = deprotocol
        socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5, '127.0.0.1', 9050)
        self.sock = sock
        self.pinger = None
        self.packet_handler = PacketHandler(sock)
        self.terminate_flag = threading.Event()
        self.handshake = False
        self.public_key, self.private_key = cf.generate_keys()
        self.connected_public_key = None
        self.connected_address = None
        self.user = User()

    def start(self):
        super().start()
        self.pinger = Pinger(self)
        self.pinger.start()
        self.send_packet(
            PacketFactory.create_packet(
                PacketType.HANDSHAKE,
                HandshakePayload(address=self.deprotocol.node.onion_address,
                                 nickname='default',
                                 profile_img='',
                                 public_key=cf.serialize_key(self.public_key)).serialize()))

    def send_packet(self, packet):
        self.packet_handler.send_packet(packet)

    def stop(self):
        self.terminate_flag.set()

    def handle_received_packet(self, received_packet):
        received_packet_handler = ReceivedPacketHandler(self)
        received_packet_handler.handle_received_packet(received_packet)

    def run(self):
        self.sock.settimeout(60.0)

        while not self.terminate_flag.is_set():
            if time.time() - self.pinger.last_ping > self.pinger.dead_time:
                self.terminate_flag.set()
                Logger.get_logger().warning("Node died")
            else:
                try:
                    received_packet = self.packet_handler.receive_packet()
                    self.handle_received_packet(received_packet)
                except socket.timeout:
                    Logger.get_logger().error("NodeConnection: timeout")
                except Exception as e:
                    self.terminate_flag.set()
                    Logger.get_logger().error("NodeConnection: Socket has been terminated")
                    Logger.get_logger().error(e)
