from deprotocol.network.protocol.packet_factory import PacketFactory
from deprotocol.network.protocol.packets.packet import Packet
from deprotocol.network.protocol.type import PacketType


class EndConnectionPacket(Packet):
    TYPE = PacketType.END_CONNECTION

    def __init__(self, payload=''):
        super().__init__(self.TYPE, 0, payload)

    @classmethod
    def from_packet(cls, packet):
        if packet.type != cls.TYPE:
            raise ValueError('Packet type does not match')
        return cls()


PacketFactory.register_packet_type(PacketType.END_CONNECTION, 'deprotocol.network.protocol.packets.end', 'EndConnectionPacket')
