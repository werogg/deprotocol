import json

from deprotocol.app.message import Message
from deprotocol.event.events.message_received_event import MessageReceivedEvent
from deprotocol.network.peer_networking.handler.packet_type_handler import PacketTypeHandler


class MessagePacketHandler(PacketTypeHandler):
    def __init__(self, node_connection):
        self.node_connection = node_connection

    def handle_packet_type(self, received_packet):
        payload = json.loads(received_packet.payload)
        self.node_connection.messages.append(Message(time=payload['time'], message=payload['message']))

        event = MessageReceivedEvent(received_packet)
        self.node_connection.deprotocol.listeners.fire(event)
