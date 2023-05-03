from deprotocol.network.protocol import PacketEncoder


class PacketSender:

    def __init__(self, sock):
        self.sock = sock
        self.packet_encoder = PacketEncoder()

    def send_packet(self, packet):
        encoded_packet = self.packet_encoder.encode_packet(packet)
        self.sock.sendall(encoded_packet)
