from unittest.mock import MagicMock
from deprotocol.protocol.packets.end import EndConnectionPacket
from deprotocol.protocol.packets.file import FileTransferPacket
from deprotocol.protocol.packets.handshake import HandshakePacket
from deprotocol import KeepAlivePacket
from deprotocol.protocol.packets.message import MessagePacket
from deprotocol.protocol.type import PacketType
from deprotocol import PacketFactory


class TestPacketFactory:

    def test_create_handshake_packet(self):
        packet = PacketFactory.create_packet(PacketType.HANDSHAKE, 'test')
        assert isinstance(packet, HandshakePacket)
        assert packet.payload == 'test'

    def test_create_message_packet(self):
        payload = 'test'
        packet = PacketFactory.create_packet(PacketType.MESSAGE, payload)
        packet.sequence_number = 123
        assert isinstance(packet, MessagePacket)
        assert 123 == packet.sequence_number
        assert payload == packet.payload

    def test_create_file_packet(self):
        payload = b'test'
        packet = PacketFactory.create_packet(PacketType.FILE, payload)
        assert isinstance(packet, FileTransferPacket)
        assert packet.payload == payload

    def test_create_keep_alive_packet(self):
        packet = PacketFactory.create_packet(PacketType.KEEP_ALIVE)
        packet.sequence_number = 0
        assert isinstance(packet, KeepAlivePacket)

    def test_create_end_connection_packet(self):
        packet = PacketFactory.create_packet(PacketType.END_CONNECTION)
        assert isinstance(packet, EndConnectionPacket)

    def test_register_packet_type(self):
        packet_type = PacketType.MESSAGE
        creator_fn = MagicMock()

        PacketFactory.register_packet_type(packet_type, creator_fn.__class__.__module__, creator_fn)

        assert PacketFactory._packet_classes[packet_type] == (creator_fn.__class__.__module__, creator_fn)
