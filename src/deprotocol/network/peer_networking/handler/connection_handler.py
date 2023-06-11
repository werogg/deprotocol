import errno
import socket
import threading

import socks

from deprotocol.app.logger import Logger
from deprotocol.network.peer_networking.node_connection import NodeConnection
from deprotocol.network.peer_networking.proxied_socket import Socket
from deprotocol.settings import PROXY_HOST
from deprotocol.settings import PROXY_PORT
from deprotocol.settings import PROXY_TYPE


class ConnectionHandler(threading.Thread):
    def __init__(self, deprotocol, network_manager):
        super().__init__()
        self.deprotocol = deprotocol
        self.network_manager = network_manager
        self.terminate_flag = threading.Event()

    def connect_to(self, address, port, initiator=False):
        sock = socks.socksocket()
        sock.settimeout(120)
        sock.setproxy(PROXY_TYPE, PROXY_HOST, PROXY_PORT)

        Logger.get_logger().info(f"connecting to {address} port {port}")

        try:
            sock.connect((address, port))
        except Exception as exc:
            Logger.get_logger().error(exc)

        Logger.get_logger().info(
            f"NodeConnection.send: Started with client ({address}) ':{str(port)}'"
        )
        new_connection = self.create_new_connection(self.deprotocol, sock, initiator)
        new_connection.start()

        return new_connection

    def run(self):
        with Socket(self.network_manager.host, self.network_manager.port) as sock:
            while not self.terminate_flag.is_set():
                try:
                    conn, _ = sock.accept()
                    new_connection = self.create_new_connection(self.deprotocol, conn, False)
                    self.network_manager.node_connections.append(new_connection)
                    Logger.get_logger().info("Connection created with a client.")
                    new_connection.start()
                except socket.timeout:
                    continue
                except socket.error as exc:
                    if exc.errno == errno.ECONNRESET:
                        Logger.get_logger().error(f"SocketClosed: {str(exc)}")
                except Exception as exc:
                    Logger.get_logger().error(exc)
            self.stop()

    def create_new_connection(self, deprotocol, conn, initiator=False):
        return NodeConnection(deprotocol, conn, len(self.network_manager.node_connections), initiator)

    def stop(self):
        self.terminate_flag.set()
        self.close_all_connections()

    def close_all_connections(self):
        for conn in self.network_manager.node_connections:
            if conn:
                conn.stop()
