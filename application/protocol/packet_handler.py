import asyncio

from application.protocol.packets.handshake import HandshakePacket
from application.protocol import PacketEncoder, PacketDecoder
from application.protocol.packet_factory import PacketFactory
from application.protocol.type import PacketType


class PacketHandler:
    def __init__(self, reader: asyncio.StreamReader, writer: asyncio.StreamWriter):
        self.reader = reader
        self.writer = writer
        self.receive_buffer = bytearray()
        self.send_buffer = bytearray()
        self.sequence_number = 0
        self.packet_encoder = PacketEncoder()
        self.packet_decoder = PacketDecoder()

    async def send_packet(self, packet: HandshakePacket) -> None:
        packet.sequence_number = self.sequence_number
        encoded_packet = self.packet_encoder.encode_packet(packet)
        self.writer.write(encoded_packet)
        self.sequence_number += 1
        await self.writer.drain()

    # TODO: change function output and condition
    async def receive_packet(self):
        data = await self.reader.read(4096)
        if not data:
            raise ConnectionError('Connection closed by peer')
        self.receive_buffer.extend(data)
        if packet := self.packet_decoder.decode_packet(self.receive_buffer):
            self.receive_buffer = self.receive_buffer[packet.size:]
            return pack
        return None

    # TODO: add async func
    def send_file(self, file_path: str) -> None:
        with open(file_path, 'rb') as f:
            for data in iter(lambda: f.read(4096), b''):
                packet = PacketFactory.create_packet(payload=data)
                self.send_packet(packet)
        self.send_packet(PacketFactory.create_packet(''))

    def receive_file(self, file_path: str) -> None:
        with open(file_path, 'wb') as f:
            packet = self.receive_packet()
            while packet.TYPE is not PacketType.END_FILE:
                if packet.TYPE != PacketType.FILE:
                    raise ValueError(f'Unexpected packet type: {packet.TYPE}')
                f.write(packet.data)
            print('File written')
