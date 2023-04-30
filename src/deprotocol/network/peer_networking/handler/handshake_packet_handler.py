import json

from deprotocol.network.peer_networking.handler.packet_type_handler import PacketTypeHandler


class HandshakePacketHandler(PacketTypeHandler):
    def __init__(self, node_connection):
        self.node_connection = node_connection

    def handle_packet_type(self, received_packet):
        payload = json.loads(received_packet.payload)
        self.node_connection.connected_address = payload['address']
        self.node_connection.user.nickname = payload['nickname']
        self.node_connection.user.profile_img = payload['profile_img']
        self.node_connection.connected_public_key = payload['public_key']
        self.node_connection.handshake = True
