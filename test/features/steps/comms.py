import threading
import time
from asyncio import Event

from behave import *
from deprotocol.api.client import Client
from deprotocol.event.event_listener import Listener
from deprotocol.event.events.deprotocol_ready_event import DeProtocolReadyEvent
from deprotocol.event.events.handshake_received_event import HandshakeReceivedEvent
from deprotocol.event.events.message_received_event import MessageReceivedEvent
from deprotocol.event.events.packet_received_event import PacketReceivedEvent
from deprotocol.network.protocol.type import PacketType
from deprotocol.settings import TEST_SLOW_TIMEOUT


class DeProtocolReadyListener(Listener):
    def __init__(self):
        self.event = Event()

    def handle_event(self, event: DeProtocolReadyEvent):
        self.event.set()


class HandshakeOneListeners(Listener):
    def __init__(self):
        self.event = threading.Event()
        self.received_event = None

    def handle_event(self, event: HandshakeReceivedEvent):
        self.received_event = event
        self.event.set()


class HandshakeTwoListeners(Listener):
    def __init__(self):
        self.event = threading.Event()
        self.received_event = None

    def handle_event(self, event: HandshakeReceivedEvent):
        self.received_event = event
        self.event.set()


class PacketReceivedListener(Listener):
    def __init__(self):
        self.event = threading.Event()
        self.received_event = None

    def handle_event(self, event: PacketReceivedEvent):
        self.received_event = event
        self.event.set()


class MessageReceivedListener(Listener):
    def __init__(self):
        self.event = threading.Event()
        self.received_event = None

    def handle_event(self, event: MessageReceivedEvent):
        self.received_event = event
        self.event.set()


@given('two clients of DeProtocol')
def step_impl(context):
    context.deprotocol_client1 = Client(testing=True)
    context.deprotocol_client2 = Client(testing=True)
    context.ready_client1 = DeProtocolReadyListener()
    context.ready_client2 = DeProtocolReadyListener()
    context.handshake_client1 = HandshakeOneListeners()
    context.handshake_client2 = HandshakeTwoListeners()
    context.message_client2 = MessageReceivedListener()

    context.deprotocol_client1.register_listener(context.ready_client1)
    context.deprotocol_client2.register_listener(context.ready_client2)

    context.deprotocol_client1.register_listener(context.handshake_client1)
    context.deprotocol_client2.register_listener(context.handshake_client2)

    context.deprotocol_client2.register_listener(context.message_client2)


@when('the clients are started')
def step_when_clients_started(context):
    context.deprotocol_client1.start()
    context.deprotocol_client2.start()


@then('wait until both clients are ready to establish a connection')
def step_then_wait_both_clients_ready(context):
    start_time = time.time()
    while not context.ready_client1.event.is_set() and context.ready_client2.event.is_set():
        elapsed_time = time.time() - start_time
        if elapsed_time >= TEST_SLOW_TIMEOUT:
            raise TimeoutError("Timeout while waiting for both clients to be ready")
        time.sleep(0.1)
    print("READY")


@when('a client initiates a connection to the other client')
def step_when_client_connect_other_client(context):
    context.deprotocol_client2.connect(context.deprotocol_client1.get_address())


@then('perform a secure handshake with the peer')
def step_then_perform_handshake(context):
    pass


@when('the handshake is successfully completed')
def step_when_handshake_success(context):
    while not context.handshake_client1.event.is_set() and context.handshake_client2.event.is_set():
        pass


@then('validate the authenticity and integrity of the handshake packet')
def step_then_validate_handshake(context):
    assert context.handshake_client1.received_event.packet.TYPE == PacketType.HANDSHAKE
    assert context.handshake_client2.received_event.packet.TYPE == PacketType.HANDSHAKE


@when('a message is sent to the peer')
def step_when_send_message_to_peer(context):
    context.deprotocol_client1.send_message(0, "This is test message")


@then('the peer receives the message')
def step_then_validate_message(context):
    while not context.message_client2.event.is_set():
        pass


@when('the message is successfully validated')
def step_when_message_validated(context):
    assert context.message_client2.received_event.message == "This is test message"


@then('stop the clients')
def step_finally_stop_the_clients(context):
    context.deprotocol_client1.stop()
    context.deprotocol_client2.stop()
