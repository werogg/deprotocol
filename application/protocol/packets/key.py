from application.protocol.packets.packet import Packet


class PublicKeyExchangePacket(Packet):
    TYPE = 2

    def __init__(self, public_key):
        super().__init__(self.TYPE, 0, public_key)

    @classmethod
    def from_packet(cls, packet):
        if packet.type != cls.TYPE:
            raise ValueError('Packet type does not match')
        return cls(packet.payload)