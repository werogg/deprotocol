from application.protocol.packets.end import EndConnectionPacket
from application.protocol.packets.file import FileTransferPacket
from application.protocol.packets.handshake import HandshakePacket
from application.protocol.packets.keepalive import KeepAlivePacket
from application.protocol.packets.message import MessagePacket
from application.protocol.type import PacketType


class PacketFactory:

    _creators = {}

    @classmethod
    def register_packet_type(cls, packet_type, creator_fn):
        cls._creators[packet_type] = creator_fn

    @classmethod
    def create_packet_abs(cls, packet_type, payload):
        creator_fn = cls._creators.get(packet_type)
        if not creator_fn:
            raise ValueError('Invalid packet type')
        return creator_fn(payload)

    @staticmethod
    def create_packet(packet_type, payload):
        if packet_type == PacketType.HANDSHAKE:
            return HandshakePacket(payload)
        elif packet_type == PacketType.MESSAGE:
            sequence_number, message = payload
            return MessagePacket(sequence_number, message)
        elif packet_type == PacketType.FILE:
            file_data = payload
            return FileTransferPacket(file_data)
        elif packet_type == PacketType.KEEP_ALIVE:
            return KeepAlivePacket()
        elif packet_type == PacketType.END_CONNECTION:
            return EndConnectionPacket()
        else:
            raise ValueError('Invalid packet type')