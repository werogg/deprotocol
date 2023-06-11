from deprotocol.network.protocol.packets.packet import Packet
from deprotocol.network.protocol.type import PacketType


class HandshakePacket(Packet):
    TYPE = PacketType.HANDSHAKE

    def __init__(self, payload=None):
        super().__init__(self.TYPE, 0, payload)
