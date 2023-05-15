import errno
import hashlib
import json
import socket
import asyncio
import time

import socks
import stem

from siosocks.io.asyncio import open_connection
from siosocks.io.asyncio import socks_server_handler

from application.logger.logger import Logger
from application.p2p.handler.connection_handler import ConnectionHandler
from application.p2p.node_connection import NodeConnection
from application.p2p.pinger import Pinger
from application.p2p.proxied_socket import Socket
from application.settings import NODE_PORT
from application.settings import PROXY_PORT, PROXY_HOST
from application.settings import CONTROL_PORT
from application.utils import crypto_funcs as cf
from application.utils.tor_utils import TorUtils



class Node:

    def __init__(self, host='', port: int = NODE_PORT, onion_address=''):
        # self.packet_handler = None
        self.terminate_flag = asyncio.Event()
        self.loop = asyncio.get_running_loop()
        self.dead_time = 100
        self.host = host
        self.port = port
        self.onion_address = onion_address

        self.node_connections = []
        self.msgs = {}
        self.banned_address = []

        self.public_key, self.private_key = cf.generate_keys()
        self.id = cf.serialize_key(self.public_key)

        self.pinger = Pinger(self)

    async def start(self) -> None:
        server = await asyncio.start_server(self.handle_connection,
                                            self.host, self.port)
        asyncio.create_task(self._serve(server))

    async def _serve(self, server: asyncio.AbstractServer) -> None:
        async with server:
            Logger.get_instance().info(f'Serving on {self.host}:{self.port}\n')
            await server.serve_forever()

    async def handle_connection(self, reader: asyncio.StreamReader, writer: asyncio.StreamWriter) -> None:
        addr = writer.get_extra_info("peername")
        connection_handler = ConnectionHandler(reader, writer, addr, self)
        asyncio.create_task(connection_handler.start())

    async def connect(self, host: str, port: int) -> None:
        if self.is_valid_address(host):
            await TorUtils.establish_tor_connection()
            try:
                reader, writer = await open_connection(host, 80, socks_host=PROXY_HOST,
                                                       socks_port=PROXY_PORT, socks_version=5)
                Logger.get_instance().info(f"Connected to {host} port {port}")
            except Exception as exs:
                Logger.get_instance().error(exs)
                return

            connection_handler = ConnectionHandler(reader, writer, (host, port), self)
            # self.loop.create_task(connection_handler.start())
            await connection_handler.start()

    def is_valid_address(self, address: str) -> bool:
        if address is self.host or address in self.banned_address:
            return False
        for node in self.node_connections:
            if node.connected_host == self.host:
                Logger.get_instance().info("Already connected with this node.")
                return False

        return True

    def stop(self) -> None:
        self.terminate_flag.set()

    def node_connected(self, node: NodeConnection) -> None:
        Logger.get_instance().info(f"Connected to node: {node.connected_host}")
        if node.connected_host not in self.node_connections:
            self.node_connections.append(node.connected_host)

    ''' 
    TODO: All methods from here until final of the file are methods that breaks SOLID.
    They must be refactored ASAP so we separate responsibilities.
    '''
    async def network_send(self, message: dict, exc=[]) -> None:
        for node_ in self.node_connections:
            if node_.connected_host in exc:
                pass
            else:
                await node_.send(json.dumps(message))

    def recieve_message_from_node(self, node, data: str) -> None:
        try:
            json.loads(data)
        except json.decoder.JSONDecodeError:
            Logger.get_instance().error(f"Error loading message from {node.id}")
            return
        self.data_handler(json.loads(data), [node.connected_host, self.host])

    async def message(self, type: str, data: str, overides={}, ex=[]) -> None:
        # time that the message was sent
        dict = {"type": type, "data": data}
        if "time" not in dict:
            dict["time"] = str(time.time())

        if "snid" not in dict:
            # sender node id
            dict["snid"] = str(self.id)

        if "rnid" not in dict:
            # reciever node id
            dict["rnid"] = None

        if "sig" not in dict:
            dict["sig"] = cf.sign(data, self.private_key)

        dict = {**dict, **overides}
        await self.network_send(dict, ex)

    async def start_pinger(self):
        await self.pinger.start()

    def stop_pinger(self):
        self.pinger.stop()

    # TODO: change the structure of the lower functions under SOLID
    @staticmethod
    def check_validity(msg: dict) -> bool:
        if not (
                "time" in msg
                and "type" in msg
                and "snid" in msg
                and "sig" in msg
                and "rnid" in msg
        ):
            return False

        if not cf.verify(msg["data"], msg["sig"], cf.load_key(msg["snid"])):
            Logger.get_instance().info(
                f"Error validating signature of message from {msg['snid']}"
            )
            return False

        if msg["type"] == "resp":
            if "ip" not in msg and "localip" not in msg:
                return False
        return True

    def encryption_handler(self, dta: dict):
        if dta["rnid"] == self.id:
            dta["data"] = cf.decrypt(dta["data"], self.private_key)
            return dta
        elif dta["rnid"] is None:
            return dta
        else:
            return False

    def on_message(self, data: str, sender, private) -> None:
        Logger.get_instance().info("Incomig Message: " + data)

    def data_handler(self, dta: dict, n) -> bool:
        if not Node.check_validity(dta):
            return False

        data = self.encryption_handler(dta)

        if not dta:
            return False

        type = data["type"]
        data = data["data"]

        if type == "msg":
            self.on_message(data, dta["snid"], bool(dta["rnid"]))

    def node_disconnected(self, node) -> None:
        Logger.get_instance().info("Disconnected from: " + node.connected_host)
        if node.connected_host in self.node_connections:
            self.node_connections.remove(node.connected_host)
