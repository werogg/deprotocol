from deprotocol.app.logger import Logger
from deprotocol.network.protocol import PacketDecoder


class PacketReceiver:
    def __init__(self, sock, decrypter):
        self.sock = sock
        self.receive_buffer = bytearray()
        self.packet_decoder = PacketDecoder()
        self.packet_decrypter = decrypter

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
