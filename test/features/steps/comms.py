import threading
import time
from asyncio import Event

from behave import *
from deprotocol.api.client import Client
from deprotocol.event.event_listener import Listener
from deprotocol.event.events.deprotocol_ready_event import DeProtocolReadyEvent
from deprotocol.event.events.packet_received_event import PacketReceivedEvent
from deprotocol.network.protocol.type import PacketType


class DeProtocolReadyListener(Listener):
    def __init__(self):
        self.event = Event()

    def handle_event(self, event: DeProtocolReadyEvent):
        self.event.set()


class PacketReceivedListener(Listener):
    def __init__(self):
        self.event = threading.Event()
        self.received_event = None

    def handle_event(self, event: PacketReceivedEvent):
        self.received_event = event
        self.event.set()


@given('two clients of DeProtocol')
def step_impl(context):
    context.deprotocol_client1 = Client()
    context.deprotocol_client2 = Client()
    listener = DeProtocolReadyListener()
    context.listener2 = PacketReceivedListener()
    context.listener3 = PacketReceivedListener()

    context.deprotocol_client1.register_listener(listener)
    context.deprotocol_client2.register_listener(listener)

    context.deprotocol_client1.register_listener(context.listener2)
    context.deprotocol_client2.register_listener(context.listener3)

    context.deprotocol_client1.start()
    context.deprotocol_client2.start()


@when('a client connects to another client')
def step_when_client_connect_other_client(context):
    context.deprotocol_client2.connect(context.deprotocol_client1.get_address())


@then('they do a handshake')
def step_then_they_do_a_handshake(context):
    while not context.listener2.event.is_set() and context.listener3.event.is_set():
        pass
    assert context.listener2.received_event.packet.TYPE == PacketType.HANDSHAKE

    context.deprotocol_client1.send_message(0, "pene")
    time.sleep(2)


@then('stop the clients')
def step_finally_stop_the_clients(context):
    context.deprotocol_client1.stop()
    context.deprotocol_client2.stop()
