class PacketEncoder:
    @staticmethod
    def encode_packet(packet):
        return packet.to_bytes()
