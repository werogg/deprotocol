class MessageHandler:

    def __init__(self):
        self.message_callbacks = []

    def add_message_callback(self, callback):
        self.message_callbacks.append(callback)

    def remove_message_callback(self, callback):
        self.message_callbacks.remove(callback)

    def handle_message(self, peer, message):
        for callback in self.message_callbacks:
            callback(peer, message)
