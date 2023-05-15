import asyncio
import json
import socket
import sys
import threading
import time
from collections import deque

import socks

from application.logger.logger import Logger
from application.utils import crypto_funcs as cf
# from application.p2p.node import Node


class NodeConnection:

    def __init__(self, main_node, reader: asyncio.StreamReader, writer: asyncio.StreamWriter, id: str, host: str, port: int):
        self.connected_host = host
        self.connected_port = port
        self.main_node = main_node
        self.reader = reader
        self.writer = writer
        self.terminate_flag = asyncio.Event()
        self.last_ping = time.time()
        # Variable for parsing the incoming json messages
        self.buffer = ""

        # The id of the connected node
        self.public_key = cf.load_key(id)
        self.id = id

        Logger.get_instance().info(
            "NodeConnection.send: Started with client ("
            + self.connected_host
            + ")"
            + ":"
            + str(self.connected_port)
            + ""
        )

    async def stop(self) -> None:
        await self.disconnect_nodes()
        self.terminate_flag.set()

    def is_first_peer(self) -> bool:
        if len(self.main_node.node_connections) > 1:
            return False
        return True

    # BUG: always returns True
    def is_node_dead(self):
        return time.time() - self.last_ping > self.main_node.dead_time

    async def start(self) -> None:
        if self.is_first_peer():
            asyncio.create_task(self.main_node.start_pinger())
        await self._run()

    async def _run(self):

        while not self.terminate_flag.is_set():
            # if self.is_node_dead:
            #     await self.stop()
            #     Logger.get_instance().warning(f"node {self.id} is dead")

            line = await self.receive_packet()
            if line != "":
                self.handle_buffer_overflow(line)
                # Get the messages by finding the message ending -TSN
                index = self.buffer.find("-TSN")
                while index > 0:
                    index = self.process_message_from_buffer(index)

            await asyncio.sleep(0.01)

        await self.stop()

    async def send(self, data: json.JSONEncoder) -> None:
        try:
            data = f"{data}-TSN"
            self.writer.write(data.encode('utf-8'))
            await self.writer.drain()

        except ConnectionResetError:
            Logger.get_instance().error("Connection is lost")
            await self.stop()

        except Exception as e:
            Logger.get_instance().error(
                "NodeConnection.send: Unexpected ercontent/ror:"
                + str(sys.exc_info()[0])
            )
            Logger.get_instance().error(f"Exception: {str(e)}")
            await self.stop()

    async def receive_packet(self):
        try:
            line = await self.reader.read(4096)
        except Exception as e:
            self.terminate_flag.set()
            Logger.get_instance().error(
                f"NodeConnection: Socket has been terminated ({e})"
            )
            Logger.get_instance().error(e)
            return ""
        return line

    def handle_buffer_overflow(self, line):
        try:
            self.buffer += str(line.decode("utf-8"))
        except Exception as e:
            print(f"NodeConnection: Decoding line error | {str(e)}")

    def process_message_from_buffer(self, index):
        message = self.buffer[:index]
        self.buffer = self.buffer[index + 4::]

        if message == "ping":
            self.last_ping = time.time()
        else:
            self.main_node.recieve_message_from_node(self, message)

        return self.buffer.find("-TSN")

    async def disconnect_nodes(self):
        if self.is_first_peer():
            self.main_node.stop_pinger()

        self.main_node.node_disconnected(self)
        self.writer.close()
        del self.main_node.node_connections[self.main_node.node_connections.index(self)]
        await asyncio.sleep(1)
