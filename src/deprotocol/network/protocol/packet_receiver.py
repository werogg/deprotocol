from deprotocol.network.protocol import PacketDecoder


class PacketReceiver:
    def __init__(self, sock):
        self.receive_buffer = None
        self.sock = sock
        self.receive_bugger = bytearray()
        self.packet_decoder = PacketDecoder()

    def receive_packet(self):
        data = self.sock.recv(4096)
        if not data:
            raise ConnectionError('Connection closed by peer')
        self.receive_buffer.extend(data)
        if packet := self.packet_decoder.decode_packet(self.receive_buffer):
            self.receive_buffer = self.receive_buffer[packet.size:]
            return packet
        return None
