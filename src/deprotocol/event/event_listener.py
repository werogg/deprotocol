from abc import ABC
from abc import abstractmethod
from inspect import signature

from deprotocol.event.events.event import Event


class Listener(ABC):
    @abstractmethod
    def handle_event(self, event):
        pass


class Listeners:
    def __init__(self):
        self.listeners = {}

    def register_listener(self, listener):
        if not isinstance(listener, Listener):
            raise ValueError("Listener must be an instance of Listener")

        event_type = self._get_event_type(listener)
        self.listeners.setdefault(event_type, []).append(listener.handle_event)

    def fire(self, event):
        if not isinstance(event, Event):
            raise ValueError("Event must be an instance of Event")

        for listener_fn in self.listeners.get(type(event), []):
            listener_fn(event)

    def _get_event_type(self, listener):
        # Get the signature of the listener's notify method
        sig = signature(listener.handle_event)
        params = sig.parameters.values()

        # Find the first parameter with a type that is a subclass of Event
        for param in params:
            if param.annotation is not param.empty and issubclass(param.annotation, Event):
                return param.annotation

        raise ValueError("Listener's handle event method must have an argument that is a subclass of Event")