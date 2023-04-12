from application.protocol.packets.packet import Packet
from application.protocol.type import PacketType


class KeepAlivePacket(Packet):
    TYPE = PacketType.KEEP_ALIVE

    def __init__(self):
        super().__init__(self.TYPE, 0, b'')

    @classmethod
    def from_packet(cls, packet):
        if packet.type != cls.TYPE:
            raise ValueError('Packet type does not match')
        return cls()