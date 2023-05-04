from deprotocol.network.protocol.packets.packet import Packet
from deprotocol.network.protocol.type import PacketType


class FileTransferPacket(Packet):
    TYPE = PacketType.FILE

    def __init__(self, chunk_data, filename='xd'):
        super().__init__(self.TYPE, 0, chunk_data)
        self.filename = filename

    @classmethod
    def from_packet(cls, packet):
        if packet.type != cls.TYPE:
            raise ValueError('Packet type does not match')
        return cls(packet.payload, packet.filename)


class FileTransferEndPacket(Packet):
    TYPE = PacketType.END_FILE

    def __init__(self):
        super().__init__(self.TYPE, 0, '')

    @classmethod
    def from_packet(cls, packet):
        if packet.type != cls.TYPE:
            raise ValueError('Packet type does not match')
        return cls()