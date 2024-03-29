import socket
import threading
import time

import socks

from deprotocol.app.user import User
from deprotocol.app.logger import Logger
from deprotocol.app.user import UserHelper
from deprotocol.network.peer_networking.handler.received_packet_handler import ReceivedPacketHandler
from deprotocol.network.peer_networking.pinger import Pinger
from deprotocol.network.protocol.packet_factory import PacketFactory
from deprotocol.network.protocol.packet_handler import PacketHandler
from deprotocol.network.protocol.payloads.handshake_payload import HandshakePayload
from deprotocol.network.protocol.payloads.message_payload import MessagePayload
from deprotocol.network.protocol.type import PacketType
from deprotocol.utils import crypto_funcs as cf
from deprotocol.utils.message_authenticator import MessageAuthenticator


class NodeConnection(threading.Thread):
    def __init__(self, deprotocol, sock, node_id, initiator=False):
        super().__init__()
        self.id = node_id
        self.deprotocol = deprotocol
        socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5, '127.0.0.1', 9050)
        self.sock = sock
        self.pinger = None
        self.terminate_flag = threading.Event()
        self.handshake = False
        self.public_key, self.private_key = cf.generate_keys()
        self.connected_public_key = None
        self.connected_address = None
        self.initiator = initiator
        self.user = UserHelper.get_user_helper().get_user()
        self.messages = []
        self.packet_handler = PacketHandler(sock, self.private_key)
        self.closed = False

    def start(self):
        self.pinger = Pinger(self)
        self.pinger.start()
        self.send_packet(
            PacketFactory.create_packet(
                PacketType.HANDSHAKE,
                HandshakePayload(address=self.deprotocol.node.onion_address,
                                 nickname=self.user.nickname,
                                 profile_img=self.user.profile_img,
                                 public_key=cf.serialize_key(self.public_key),
                                 initiator=self.initiator).serialize()))
        super().start()

    def send_packet(self, packet):
        if not self.closed:
            self.packet_handler.send_packet(packet)
        else:
            Logger.get_logger().warning("Trying to send a packet to a closed socket.")

    def send_message(self, message):
        self.send_packet(PacketFactory.create_packet(
            PacketType.MESSAGE,
            MessagePayload(message,
                           MessageAuthenticator.sign_message(message, self.private_key)).serialize()
        ))

    def stop(self):
        self.terminate_flag.set()
        self.pinger.stop()
        self.sock.close()
        self.closed = True

    def handle_received_packet(self, received_packet):
        received_packet_handler = ReceivedPacketHandler(self)
        received_packet_handler.handle_received_packet(received_packet)

    def run(self):
        self.sock.settimeout(30.0)

        while not self.terminate_flag.is_set():
            if time.time() - self.pinger.last_ping > self.pinger.dead_time:
                self.terminate_flag.set()
                Logger.get_logger().warning(f"Socket {self.id} died")
            else:
                try:
                    received_packet = self.packet_handler.receive_packet()
                    self.handle_received_packet(received_packet)
                except socket.timeout:
                    Logger.get_logger().error(f"NodeConnection: Socket {self.id} timeout")
                    self.stop()
                except Exception as e:
                    Logger.get_logger().error(f"NodeConnection: Socket {self.id} has been terminated -> {e}")
                    self.stop()
