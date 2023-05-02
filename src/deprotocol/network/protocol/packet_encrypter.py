from deprotocol.network.protocol.type import PacketType
from deprotocol.utils import crypto_funcs as cf


class PacketEncrypter:
    def __init__(self):
        self.public_key = None

    def populate_public_key(self, key):
        self.public_key = key

    def encrypt_packet(self, packet, encoded_packet):
        if packet.TYPE is not PacketType.HANDSHAKE and packet.TYPE is not PacketType.KEEP_ALIVE:
            return cf.encrypt(encoded_packet, cf.load_key(self.public_key))
        return encoded_packet
