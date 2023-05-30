from deprotocol.utils import crypto_funcs as cf


class MessageAuthenticator:

    @staticmethod
    def sign_message(message, private_key):
        return cf.sign(message, private_key)

    @staticmethod
    def verify_message(message, signature, public_key):
        return cf.verify(message, signature, cf.load_key(public_key))
