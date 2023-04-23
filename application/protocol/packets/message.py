from application.protocol.packet_factory import PacketFactory
from application.protocol.packets.packet import Packet
from application.protocol.type import PacketType


class MessagePacket(Packet):
    TYPE = PacketType.MESSAGE

    def __init__(self, message):
        super().__init__(self.TYPE, 0, message)

    @classmethod
    def from_packet(cls, packet):
        if packet.type != cls.TYPE:
            raise ValueError('Packet type does not match')
        return cls(packet.payload)


PacketFactory.register_packet_type(PacketType.MESSAGE, 'application.protocol.packets.message', 'MessagePacket')
