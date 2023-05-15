import asyncio
from application.p2p.node_connection import NodeConnection
from application.protocol import HandshakePacket
from application.protocol.packet_handler import PacketHandler


class ConnectionHandler:
    def __init__(self, reader: asyncio.StreamReader, writer: asyncio.StreamWriter, addr: tuple, node):
        self.reader = reader
        self.writer = writer
        self.addr = addr
        self.node = node

    async def send_initial_packet(self, packet_handler: PacketHandler) -> None:
        handshake_packet = HandshakePacket(self.node.id)
        await packet_handler.send_packet(handshake_packet)

    async def start(self) -> None:

        packet_handler = PacketHandler(self.reader, self.writer)
        await self.send_initial_packet(packet_handler)

        rec = await packet_handler.receive_packet()
        connected_node_id = rec.payload.decode("utf-8")

        if self.node.id != connected_node_id:
            async_client = self.create_new_connection(
                self.reader,
                self.writer,
                connected_node_id,
                self.addr[0],
                self.addr[1],
            )

            self.node.node_connections.append(async_client)
            asyncio.create_task(async_client.start())

        else:
            self.writer.close()

    def create_new_connection(self, reader: asyncio.StreamReader, writer: asyncio.StreamWriter, id: str,
                              host: str, port: int) -> NodeConnection:

        return NodeConnection(self.node, reader, writer, id, host, port)
