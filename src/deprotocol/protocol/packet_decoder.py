from deprotocol.protocol.packet_factory import PacketFactory
from deprotocol.protocol.packets.packet import Packet
from deprotocol.protocol.type import PacketType


class PacketDecoder:
    @staticmethod
    def decode_packet(packet_bytes):
        raw_packet = Packet.from_bytes(packet_bytes)
        packet_type = PacketType.from_int(raw_packet.type)
        return PacketFactory.create_packet(packet_type=packet_type, payload=raw_packet.payload)
