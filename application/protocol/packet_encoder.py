import json

import jsonpickle as jsonpickle

from application.protocol.type import PacketType


class PacketEncoder:
    @staticmethod
    def encode_packet(packet):
        return packet.to_bytes()
