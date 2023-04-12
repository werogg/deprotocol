from application.protocol.packets.packet import Packet
from application.protocol.type import PacketType


class EndConnectionPacket(Packet):
    TYPE = PacketType.END_CONNECTION

    def __init__(self):
        super().__init__(self.TYPE, 0, b'')

    @classmethod
    def from_packet(cls, packet):
        if packet.type != cls.TYPE:
            raise ValueError('Packet type does not match')
        return cls()