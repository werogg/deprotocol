from enum import Enum


class PacketType(Enum):
    HANDSHAKE = 0
    MESSAGE = 1
    FILE = 2
    END_FILE = 3
    KEEP_ALIVE = 4
    END_CONNECTION = 5

    @staticmethod
    def from_int(int_value):
        for member in PacketType:
            if member.value == int_value:
                return member
        raise ValueError(f"No matching PacketType for value {int_value}")