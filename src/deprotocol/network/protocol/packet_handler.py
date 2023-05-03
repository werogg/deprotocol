from deprotocol.app.logger import Logger
from deprotocol.network.protocol import PacketEncoder, PacketDecoder
from deprotocol.network.protocol.packet_decrypter import PacketDecrypter
from deprotocol.network.protocol.packet_encrypter import PacketEncrypter
from deprotocol.network.protocol.packet_factory import PacketFactory
from deprotocol.network.protocol.type import PacketType
from deprotocol.utils import crypto_funcs as cf


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

    def send_packet(self, packet):
        packet.sequence_number = self.sequence_number
        encoded_packet = self.packet_encoder.encode_packet(packet)

        encrypted_packet = self.packet_encrypter.encrypt_packet(packet, encoded_packet)

        self.sock.sendall(encrypted_packet)
        Logger.get_logger().trace(f'send_packet: Sent packet [{packet}]')
        self.sequence_number += 1

    def receive_packet(self):
        data = self.sock.recv(4096)
        if not data:
            raise ConnectionError('Connection closed by peer')

        self.receive_buffer.extend(data)
        try:
            packet = self.packet_decoder.decode_packet(self.receive_buffer)
            self.receive_buffer = self.receive_buffer[packet.size:]
        except Exception:
            packet = self.packet_decrypter.decrypt_packet(self.receive_buffer)
            packet = self.packet_decoder.decode_packet(packet)
            self.receive_buffer = self.receive_buffer[len(data):]
        Logger.get_logger().trace(f'receive_packet: Received packet [{packet}]')
        return packet

    def send_file(self, file_path):
        with open(file_path, 'rb') as f:
            for data in iter(lambda: f.read(4096), b''):
                packet = PacketFactory.create_packet(PacketType.FILE, payload=data)
                self.send_packet(packet)
        self.send_packet(PacketFactory.create_packet(''))

    def receive_file(self, file_path):
        with open(file_path, 'wb') as f:
            packet = self.receive_packet()
            while packet.TYPE is not PacketType.END_FILE:
                if packet.TYPE != PacketType.FILE:
                    raise ValueError(f'Unexpected packet type: {packet.TYPE}')
                f.write(packet.data)
            print('File written')
