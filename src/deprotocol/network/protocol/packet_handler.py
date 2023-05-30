from deprotocol.app.logger import Logger
from deprotocol.network.protocol import PacketEncoder, PacketDecoder
from deprotocol.network.protocol.packet_decrypter import PacketDecrypter
from deprotocol.network.protocol.packet_encrypter import PacketEncrypter
from deprotocol.network.protocol.packet_receiver import PacketReceiver
from deprotocol.network.protocol.packet_sender import PacketSender
from deprotocol.network.protocol.type import PacketType


class PacketHandler:
    def __init__(self, sock, private_key):
        self.sock = sock
        self.public_key = None
        self.private_key = private_key
        self.receive_buffer = bytearray()
        self.send_buffer = bytearray()
        self.sequence_number = 0
        self.packet_encoder = PacketEncoder()
        self.packet_decoder = PacketDecoder()
        self.packet_encrypter = PacketEncrypter()
        self.packet_decrypter = PacketDecrypter(private_key)
        self.packet_sender = PacketSender(self.sock)
        self.packet_receiver = PacketReceiver(self.sock, self.packet_decrypter)

    def send_packet(self, packet):
        packet.sequence_number = self.sequence_number
        if packet.type == PacketType.MESSAGE:
            print("test")
        encoded_packet = self.packet_encoder.encode_packet(packet)
        encrypted_packet = self.packet_encrypter.encrypt_packet(packet, encoded_packet)
        Logger.get_logger().trace(f'send_packet: Sent packet [{packet}]')
        self.packet_sender.send_packet(encrypted_packet)
        self.sequence_number += 1

    def receive_packet(self):
        return self.packet_receiver.receive_packet()
