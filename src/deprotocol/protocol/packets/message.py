from deprotocol.protocol.packet_factory import PacketFactory
from deprotocol.protocol.packets.packet import Packet
from deprotocol.protocol.type import PacketType


class MessagePacket(Packet):
    TYPE = PacketType.MESSAGE

    def __init__(self, message):
        super().__init__(self.TYPE, 0, message)

    @classmethod
    def from_packet(cls, packet):
        if packet.type != cls.TYPE:
            raise ValueError('Packet type does not match')
        return cls(packet.payload)


PacketFactory.register_packet_type(PacketType.MESSAGE, 'deprotocol.protocol.packets.message', 'MessagePacket')
