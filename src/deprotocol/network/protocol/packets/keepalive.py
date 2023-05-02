from deprotocol.network.protocol.packet_factory import PacketFactory
from deprotocol.network.protocol.packets.packet import Packet
from deprotocol.network.protocol.type import PacketType


class KeepAlivePacket(Packet):
    TYPE = PacketType.KEEP_ALIVE

    def __init__(self, payload=''):
        super().__init__(self.TYPE, 0, payload)

    @classmethod
    def from_packet(cls, packet):
        if packet.type != cls.TYPE:
            raise ValueError('Packet type does not match')
        return cls()


PacketFactory.register_packet_type(PacketType.KEEP_ALIVE, 'deprotocol.network.protocol.packets.keepalive', 'KeepAlivePacket')