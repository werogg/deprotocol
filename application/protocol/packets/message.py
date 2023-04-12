from application.protocol.packets.packet import Packet
from application.protocol.type import PacketType


class MessagePacket(Packet):
    TYPE = PacketType.MESSAGE

    def __init__(self, sequence_number, message):
        super().__init__(self.TYPE, sequence_number, message)

    @classmethod
    def from_packet(cls, packet):
        if packet.type != cls.TYPE:
            raise ValueError('Packet type does not match')
        return cls(packet.sequence_number, packet.payload)