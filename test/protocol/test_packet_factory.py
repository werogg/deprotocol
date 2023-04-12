from unittest.mock import MagicMock
from application.protocol.packets.end import EndConnectionPacket
from application.protocol.packets.file import FileTransferPacket
from application.protocol.packets.handshake import HandshakePacket
from application.protocol.packets.keepalive import KeepAlivePacket
from application.protocol.packets.message import MessagePacket
from application.protocol.type import PacketType
from application.protocol.packet_factory import PacketFactory


class TestPacketFactory:

    def test_create_handshake_packet(self):
        packet = PacketFactory.create_packet(PacketType.HANDSHAKE, 'test')
        assert isinstance(packet, HandshakePacket)
        assert packet.payload == 'test'

    def test_create_message_packet(self):
        payload = (123, 'test')
        packet = PacketFactory.create_packet(PacketType.MESSAGE, payload)
        assert isinstance(packet, MessagePacket)
        assert packet.sequence_number == payload[0]
        assert packet.payload == payload[1]

    def test_create_file_packet(self):
        payload = b'test'
        packet = PacketFactory.create_packet(PacketType.FILE, payload)
        assert isinstance(packet, FileTransferPacket)
        assert packet.payload == payload

    def test_create_keep_alive_packet(self):
        packet = PacketFactory.create_packet(PacketType.KEEP_ALIVE, None)
        assert isinstance(packet, KeepAlivePacket)

    def test_create_end_connection_packet(self):
        packet = PacketFactory.create_packet(PacketType.END_CONNECTION, None)
        assert isinstance(packet, EndConnectionPacket)

    def test_register_packet_type(self):
        packet_type = PacketType.MESSAGE
        creator_fn = MagicMock()

        PacketFactory.register_packet_type(packet_type, creator_fn)

        assert PacketFactory._creators[packet_type] == creator_fn

    def test_create_packet_abs_invalid_packet_type(self):
        packet_type = 999  # invalid packet type
        payload = (123, 'Hello, World!')

        try:
            PacketFactory.create_packet_abs(packet_type, payload)
            assert False, 'Expected ValueError to be raised'
        except ValueError:
            pass

    def test_create_packet_abs(self):
        payload = "dummy payload"
        mock_creator_fn = MagicMock()
        PacketFactory.register_packet_type(PacketType.MESSAGE, mock_creator_fn)

        PacketFactory.create_packet_abs(PacketType.MESSAGE, payload)

        mock_creator_fn.assert_called_once_with(payload)
