import struct


class Packet:
    HEADER_LENGTH = 8  # length of the packet header in bytes
    PROTOCOL_VERSION = 1

    def __init__(self, packet_type, sequence_number, payload):
        self.type = packet_type
        self.sequence_number = sequence_number
        self.payload = payload

    @property
    def size(self):
        return self.HEADER_LENGTH + len(self.payload)

    def to_bytes(self):
        payload_length = len(self.payload)
        header = struct.pack('!BBIH', self.PROTOCOL_VERSION, self.type.value, self.sequence_number, payload_length)
        return header + self.payload.encode()

    @classmethod
    def from_bytes(cls, byte_data):
        header = byte_data[:cls.HEADER_LENGTH]
        payload = byte_data[cls.HEADER_LENGTH:]
        protocol_version, packet_type, sequence_number, payload_length = struct.unpack('!BBIH', header)
        if protocol_version != cls.PROTOCOL_VERSION:
            raise ValueError('Invalid protocol version')
        return cls(packet_type, sequence_number, payload[:payload_length])
