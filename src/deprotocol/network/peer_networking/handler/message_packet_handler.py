import datetime
import json

from deprotocol.app.logger import Logger
from deprotocol.app.message import Message
from deprotocol.event.events.message_received_event import MessageReceivedEvent
from deprotocol.network.peer_networking.handler.packet_type_handler import PacketTypeHandler


class MessagePacketHandler(PacketTypeHandler):
    def __init__(self, node_connection):
        self.node_connection = node_connection

    def handle_packet_type(self, received_packet):
        payload = json.loads(received_packet.payload)
        self.node_connection.messages.append(Message(time=payload['time'], message=payload['message']))

        timestamp_dt = datetime.datetime.fromtimestamp(float(payload['time']))
        formatted_time = timestamp_dt.strftime("%Y:%m:%d - %H:%M")

        Logger.get_logger().info(f"\nMessage from node {self.node_connection.id} received:\n"
                                 f"User: {self.node_connection.user.nickname}\n"
                                 f"Time: {formatted_time}\n"
                                 f"Message: {' '.join(payload['message'])}")

        event = MessageReceivedEvent(received_packet, self.node_connection)
        self.node_connection.deprotocol.listeners.fire(event)
