from application.protocol import PacketEncoder, PacketDecoder
from application.protocol.packet_factory import PacketFactory
from application.protocol.type import PacketType


class PacketHandler:
    def __init__(self, sock):
        self.sock = sock
        self.receive_buffer = bytearray()
        self.send_buffer = bytearray()
        self.sequence_number = 0
        self.packet_encoder = PacketEncoder()
        self.packet_decoder = PacketDecoder()

    def send_packet(self, packet):
        packet.sequence_number = self.sequence_number
        encoded_packet = self.packet_encoder.encode_packet(packet)
        self.sock.sendall(encoded_packet)
        self.sequence_number += 1

    def receive_packet(self):
        data = self.sock.recv(4096)
        if not data:
            raise ConnectionError('Connection closed by peer')
        self.receive_buffer.extend(data)
        if packet := self.packet_decoder.decode_packet(self.receive_buffer):
            self.receive_buffer = self.receive_buffer[packet.size:]
            return packet
        return None

    def send_file(self, file_path):
        with open(file_path, 'rb') as f:
            for data in iter(lambda: f.read(4096), b''):
                packet = PacketFactory.create_packet(PacketType.FILE, payload=data)
                self.send_packet(packet)
        self.send_packet(PacketFactory.create_packet(PacketType.END_FILE, ''))

    def receive_file(self, file_path):
        with open(file_path, 'wb') as f:
            packet = self.receive_packet()
            while packet.TYPE is not PacketType.END_FILE:
                if packet.TYPE != PacketType.FILE:
                    raise ValueError(f'Unexpected packet type: {packet.TYPE}')
                f.write(packet.data)
            print('File written')
