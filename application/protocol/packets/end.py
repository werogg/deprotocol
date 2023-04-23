from application.protocol.packet_factory import PacketFactory
from application.protocol.packets.packet import Packet
from application.protocol.type import PacketType


class EndConnectionPacket(Packet):
    TYPE = PacketType.END_CONNECTION

    def __init__(self, payload=''):
        super().__init__(self.TYPE, 0, payload)

    @classmethod
    def from_packet(cls, packet):
        if packet.type != cls.TYPE:
            raise ValueError('Packet type does not match')
        return cls()


PacketFactory.register_packet_type(PacketType.END_CONNECTION, 'application.protocol.packets.end', 'EndConnectionPacket')
