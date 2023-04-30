from certifi.__main__ import args


class EventHandler:
    def __init__(self, event_type):
        self.event_type = event_type

    def __call__(self, func):
        def wrapper(*args, **kwargs):
            func(*args, **kwargs)

        observer = args[0]
        observer.listeners.setdefault(self.event_type, []).append(wrapper)
        return wrapper
