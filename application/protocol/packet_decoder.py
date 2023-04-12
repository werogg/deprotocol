from application.protocol.packet_factory import PacketFactory
from application.protocol.packets.packet import Packet
from application.protocol.type import PacketType


class PacketDecoder:
    @staticmethod
    def decode_packet(packet_bytes):
        raw_packet = Packet.from_bytes(packet_bytes)
        packet_type = PacketType.from_int(raw_packet.type)
        return PacketFactory.create_packet(packet_type, raw_packet.payload)
