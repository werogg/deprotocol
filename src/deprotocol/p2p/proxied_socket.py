import socket


class Socket:
    def __init__(self, host: str, port: int):
        self.host = host
        self.port = port
        self.sock = None

    def __enter__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind((self.host, self.port))
        self.sock.settimeout(30.0)
        self.sock.listen(1)
        return self.sock

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.sock.close()