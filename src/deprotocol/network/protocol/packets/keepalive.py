from deprotocol.network.protocol.packets.packet import Packet
from deprotocol.network.protocol.type import PacketType


class KeepAlivePacket(Packet):
    TYPE = PacketType.KEEP_ALIVE

    def __init__(self, payload=''):
        super().__init__(self.TYPE, 0, payload)
