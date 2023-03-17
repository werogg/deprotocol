from network.tor_network import TorService

class TorChat:
    def __init__(self, port: int, peer_id: str, keypair, tor_port: int, tor_controller_port: int):
        self.port = port
        self.peer_id = peer_id
        self.keypair = keypair
        self.tor_port = tor_port
        self.tor_controller_port = tor_controller_port
        self.peer = None
        self.tor_service = None

    def start(self):
        self.tor_service = TorService(self.tor_port)
        self.tor_service.start()

        self.peer = PeerBuilder(PeerId.createFromHex(self.peer_id)) \
            .ports(self.port) \
            .keyPair(self.keypair) \
            .peerAddress(PeerAddress(InetAddress.getByName("127.0.0.1"), self.tor_controller_port)) \
            .behindFirewall(True) \
            .buildAndListen()