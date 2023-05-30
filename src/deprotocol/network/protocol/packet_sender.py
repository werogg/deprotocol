from deprotocol.network.protocol import PacketEncoder


class PacketSender:
    MAX_CHUNK_SIZE = 1024  # Maximum chunk size for sending data

    def __init__(self, sock):
        self.sock = sock

    def send_packet(self, packet):
        total_size = len(packet)
        bytes_sent = 0

        while bytes_sent < total_size:
            chunk = packet[bytes_sent: bytes_sent + self.MAX_CHUNK_SIZE]
            self.sock.sendall(chunk)
            bytes_sent += len(chunk)
