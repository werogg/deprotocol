from enum import Enum


class PacketType(Enum):
    HANDSHAKE = 0
    PUBLIC_KEY = 1
    MESSAGE = 2
    FILE = 3
    END_FILE = 4
    KEEP_ALIVE = 5
    END_CONNECTION = 6

    @staticmethod
    def from_int(int_value):
        for member in PacketType:
            if member.value == int_value:
                return member
        raise ValueError(f"No matching PacketType for value {int_value}")