from multiprocessing import Event

from deprotocol.api.client import Client
from deprotocol.event.event_listener import Listener
from deprotocol.event.events.deprotocol_ready_event import DeProtocolReadyEvent


class DeProtocolReadyListener(Listener):
    def __init__(self):
        self.event = Event()

    def handle_event(self, event: DeProtocolReadyEvent):
        print("DeProtocol ready! Connecting")
        self.event.set()



if __name__ == "__main__":
    deprotocol_client = Client()
    listener = DeProtocolReadyListener()
    deprotocol_client.register_listener(listener)
    deprotocol_client.start()
    listener.event.wait()

    deprotocol_client.connect(address="xd2cwgtvakfvx2ohu4px3gpjcahzv4irbo7um63iiowhhendso3d5did.onion")
