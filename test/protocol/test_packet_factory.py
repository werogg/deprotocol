import unittest
from unittest.mock import MagicMock

from deprotocol.app.application import DeProtocol
from deprotocol.network.protocol.packets.end import EndConnectionPacket
from deprotocol.network.protocol.packets.file import FileTransferPacket
from deprotocol.network.protocol.packets.keepalive import KeepAlivePacket

from deprotocol.network.protocol.packets.message import MessagePacket

from deprotocol.network.protocol import HandshakePacket

from deprotocol.network.protocol.packet_factory import PacketFactory
from deprotocol.network.protocol.type import PacketType


class TestPacketFactory(unittest.TestCase):
    def setUp(self):
        deprotocol = DeProtocol()
        deprotocol.register_default_packets()

    def test_create_handshake_packet(self):
        packet = PacketFactory.create_packet(PacketType.HANDSHAKE, 'test')

        self.assertTrue(isinstance(packet, HandshakePacket))
        self.assertEqual('test', packet.payload)

    def test_create_message_packet(self):
        payload = 'test'

        packet = PacketFactory.create_packet(PacketType.MESSAGE, payload)
        packet.sequence_number = 123

        self.assertTrue(isinstance(packet, MessagePacket))
        self.assertEqual(123, packet.sequence_number)

    def test_create_file_packet(self):
        payload = b'test'

        packet = PacketFactory.create_packet(PacketType.FILE, payload)

        self.assertTrue(isinstance(packet, FileTransferPacket))
        self.assertEqual(payload, packet.payload)

    def test_create_keep_alive_packet(self):
        packet = PacketFactory.create_packet(PacketType.KEEP_ALIVE)
        packet.sequence_number = 0

        self.assertTrue(isinstance(packet, KeepAlivePacket))

    def test_create_end_connection_packet(self):
        packet = PacketFactory.create_packet(PacketType.END_CONNECTION)
        self.assertTrue(isinstance(packet, EndConnectionPacket))

    def test_register_packet_type(self):
        packet_type = PacketType.MESSAGE
        creator_fn = MagicMock()

        PacketFactory.register_packet_type(packet_type, creator_fn.__class__.__module__, creator_fn)

        self.assertEqual((creator_fn.__class__.__module__, creator_fn), PacketFactory._packet_classes[packet_type])

    def test_create_invalid_packet(self):
        invalid_packet_type = MagicMock()

        with self.assertRaises(ValueError):
            PacketFactory.create_packet(invalid_packet_type)
