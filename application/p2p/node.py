import errno
import hashlib
import json
import socket
import threading
import asyncio
import time

import socks
import stem

from application.logger.logger import Logger
from application.p2p.handler.connection_handler import ConnectionHandler
from application.p2p.deprecated_node import PORT
from application.p2p.pinger import Pinger
from application.p2p.proxied_socket import Socket
from application.utils import crypto_funcs as cf


class Node:
    def __init__(self, host='', port=65432, onion_address=''):
        self.packet_handler = None
        self.terminate_flag = asyncio.Event()
        self.loop = asyncio.get_running_loop()
        self.dead_time = 45
        self.host = host
        self.port = port
        self.onion_address = onion_address

        self.node_connections = []
        self.msgs = {}
        self.peers = []
        self.banned_address = []

        self.public_key, self.private_key = cf.generate_keys()
        self.id = cf.serialize_key(self.public_key)

        self.pinger = Pinger(self).start()

    def node_connected(self, node):
        Logger.get_instance().info(f"Connected to node: {node.connected_host}")
        if node.connected_host not in self.peers:
            self.peers.append(node.connected_host)
        # self.send_peers()

    async def start(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.settimeout(1)
        sock.bind((self.host, self.port))
        sock.listen(1)

        while not self.terminate_flag.is_set():
            try:
                conn, addr = await self.loop.sock_accept(sock)
                connection_handler = ConnectionHandler(conn, addr, self)
                self.loop.create_task(connection_handler.start())
            except socket.timeout:
                continue
            except socket.error as exc:
                if exc.errno == errno.ECONNRESET:
                    Logger.get_instance().error("SocketClosed: %s" % str(exc))
            except Exception as exc:
                Logger.get_instance().error(exc)

    async def connect(self, host, port=PORT):
        if self.is_valid_address(host):
            sock = socks.socksocket()
            sock.settimeout(60)
            sock.setproxy(socks.PROXY_TYPE_SOCKS5, "localhost", 9050, True)

            tor_controller = stem.control.Controller.from_port(port=9051)
            await tor_controller.authenticate()
            await tor_controller.new_circuit()

            Logger.get_instance().info(f"connecting to {host} port {port}")

            await self.loop.sock_connect(sock, (host, 80))

            connection_handler = ConnectionHandler(sock, (host, port), self)
            self.loop.create_task(connection_handler.start())

    def is_valid_address(self, address):
        if address in self.banned_address:
            return False

        if address == self.host:
            return False

        if address.startswith('127.'):
            return False

        if address.startswith('192.168.'):
            return False

        if address.startswith('10.'):
            return False

        return True

    def is_valid_address(self, address):
        if address is self.host or address in self.banned_address:
            return False

        for node in self.node_connections:
            if node.connected_host == self.host:
                Logger.get_instance().info("Already connected with this node.")
                return False

        return True

    def stop(self):
        self.terminate_flag.set()

    ''' 
    TODO: All methods from here until final of the file are methods that breaks SOLID.
    They must be refactored ASAP so we separate responsibilities.
    '''
    def network_send(self, message, exc=[]):
        for i in self.node_connections:
            if i.connected_host in exc:
                pass
            else:
                i.send(json.dumps(message))

    def node_message(self, node, data):
        try:
            json.loads(data)
        except json.decoder.JSONDecodeError:
            Logger.get_instance().error(f"Error loading message from {node.id}")
            return
        self.data_handler(json.loads(data), [node.connected_host, self.host])

    def message(self, type, data, overides={}, ex=[]):
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
        self.network_send(dict, ex)

    @staticmethod
    def check_validity(msg):
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

    def encryption_handler(self, dta):
        if dta["rnid"] == self.id:
            dta["data"] = cf.decrypt(dta["data"], self.private_key)
            return dta
        elif dta["rnid"] is None:
            return dta
        else:
            return False

    def on_message(self, data, sender, private):
        Logger.get_instance().info("Incomig Message: " + data)

    def data_handler(self, dta, n):
        if not Node.check_validity(dta):
            return False

        data = self.encryption_handler(dta)

        if not dta:
            return False

        type = data["type"]
        data = data["data"]

        if type == "msg":
            self.on_message(data, dta["snid"], bool(dta["rnid"]))

    def node_disconnected(self, node):
        Logger.get_instance().info("Disconnected from: " + node.connected_host)
        if node.connected_host in self.peers:
            self.peers.remove(node.connected_host)
