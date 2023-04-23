import pytest
from unittest.mock import MagicMock, patch

from application.protocol import PacketDecoder
from application.protocol.packet_encoder import PacketEncoder
from application.protocol.packet_factory import PacketFactory
from application.protocol.packet_handler import PacketHandler
from application.protocol.type import PacketType


class TestPacketHandler:

    @pytest.fixture
    def mock_socket(self):
        return MagicMock()

    @pytest.fixture
    def packet_handler(self, mock_socket):
        return PacketHandler(mock_socket)

    def test_send_packet(self, packet_handler, mock_socket):
        packet = PacketFactory.create_packet(packet_type=PacketType.HANDSHAKE, payload='test')
        packet_handler.send_packet(packet)
        mock_socket.sendall.assert_called_once()

    def test_receive_packet(self, packet_handler, mock_socket):
        encoded_packet = PacketEncoder().encode_packet(
            PacketFactory.create_packet(packet_type=PacketType.HANDSHAKE, payload='test'))
        mock_socket.recv.return_value = encoded_packet
        packet = packet_handler.receive_packet()
        assert packet.TYPE == PacketType.HANDSHAKE

    def test_receive_packet_no_data(self, packet_handler, mock_socket):
        mock_socket.recv.return_value = b''
        with pytest.raises(ConnectionError):
            packet_handler.receive_packet()
