from application.protocol.packets.packet import Packet
from application.protocol.type import PacketType


class HandshakePacket(Packet):
    TYPE = PacketType.HANDSHAKE

    def __init__(self, public_key=None):
        super().__init__(self.TYPE, 0, public_key)

    @classmethod
    def from_packet(cls, packet):
        if packet.type != cls.TYPE:
            raise ValueError('Packet type does not match')
        return cls(packet.payload)