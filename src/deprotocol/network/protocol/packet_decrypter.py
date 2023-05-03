from deprotocol.network.protocol.type import PacketType
from deprotocol.utils import crypto_funcs as cf


class PacketDecrypter:
    def __init__(self, private_key):
        self.private_key = private_key

    def decrypt_packet(self, bytes):
        return cf.decrypt(bytes, self.private_key)

