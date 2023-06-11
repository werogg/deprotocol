from deprotocol.network.protocol.packets.packet import Packet
from deprotocol.network.protocol.type import PacketType


class MessagePacket(Packet):
    TYPE = PacketType.MESSAGE

    def __init__(self, message):
        super().__init__(self.TYPE, 0, message)