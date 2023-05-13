from application.p2p.node_connection import NodeConnection
from application.protocol import HandshakePacket
from application.protocol.packet_handler import PacketHandler


class ConnectionHandler:
    def __init__(self, conn, addr, node):
        self.conn = conn
        self.addr = addr
        self.node = node

    async def start(self):
        print("Start")
        packet_handler = PacketHandler(self.conn)

        self.send_initial_packet(packet_handler)

        rec = packet_handler.receive_packet()
        connected_node_id = rec.payload.decode("utf-8")

        if self.node.id != connected_node_id:
            thread_client = self.create_new_connection(
                self.conn,
                connected_node_id,
                self.addr[0],
                self.addr[1],
            )
            thread_client.start()

            self.node.node_connections.append(thread_client)

            self.node.node_connected(thread_client)

        else:
            self.conn.close()

    def send_initial_packet(self, packet_handler):
        handshake_packet = HandshakePacket(self.node.id)
        packet_handler.send_packet(handshake_packet)

    def create_new_connection(self, connection, id, host, port):
        return NodeConnection(self.node, connection, id, host, port)
