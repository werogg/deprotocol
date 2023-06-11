from deprotocol.network.protocol.packets.packet import Packet
from deprotocol.network.protocol.type import PacketType


class EndConnectionPacket(Packet):
    TYPE = PacketType.END_CONNECTION

    def __init__(self, payload=''):
        super().__init__(self.TYPE, 0, payload)
