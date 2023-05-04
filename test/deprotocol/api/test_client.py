import unittest
from unittest.mock import Mock
from unittest.mock import patch, MagicMock

from deprotocol.api.client import Client
from deprotocol.app.application import DeProtocol
from deprotocol.app.listeners.packet_received_listener import PacketReceivedListener


class TestClient(unittest.TestCase):

    def setUp(self):
        self.mock_node = Mock()
        self.client = Client()
        self.client.app.node = self.mock_node

    @patch.object(DeProtocol, 'on_start')
    def test_start(self, mock_on_start):
        self.client.start()
        mock_on_start.assert_called_once_with('127.0.0.1', 9050)

    @patch.object(DeProtocol, 'on_stop')
    def test_stop(self, mock_on_stop):
        self.client.stop()
        mock_on_stop.assert_called_once()

    def test_connect(self):
        self.client.connect('1.2.3.4', 9050)
        self.mock_node.connect_to.assert_called_once_with('1.2.3.4', 9050)

    def test_send_message(self):
        self.mock_node.network_manager.node_connections = [MagicMock(id=1), MagicMock(id=2)]
        self.client.send_message(2, 'hello')
        self.mock_node.network_manager.node_connections[1].send_message.assert_called_once_with('hello')

    def test_get_connected_nodes(self):
        self.mock_node.get_connected_nodes.return_value = ['node1', 'node2']
        self.assertEqual(self.client.get_connected_nodes(), ['node1', 'node2'])

    @patch.object(DeProtocol, 'register_listener')
    def test_register_listener(self, mock_register_listener):
        listener = PacketReceivedListener()
        self.client.register_listener(listener)
        mock_register_listener.assert_called_once_with(listener)

    def test_get_address(self):
        self.mock_node.onion_address = 'abcdefg.onion'
        self.assertEqual(self.client.get_address(), 'abcdefg.onion')
