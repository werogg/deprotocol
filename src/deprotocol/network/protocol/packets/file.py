from deprotocol.network.protocol.packets.packet import Packet
from deprotocol.network.protocol.type import PacketType


class FileTransferPacket(Packet):
    TYPE = PacketType.FILE

    def __init__(self, chunk_data, filename='xd'):
        super().__init__(self.TYPE, 0, chunk_data)
        self.filename = filename


class FileTransferEndPacket(Packet):
    TYPE = PacketType.END_FILE

    def __init__(self):
        super().__init__(self.TYPE, 0, '')
