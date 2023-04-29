import errno
import socket
import threading

import socks
import stem

from deprotocol.logger.logger import Logger
from deprotocol.p2p.node_connection import NodeConnection
from deprotocol.p2p.proxied_socket import Socket


class ConnectionHandler(threading.Thread):
    def __init__(self, network_manager):
        super().__init__()
        self.network_manager = network_manager
        self.terminate_flag = threading.Event()

    def connect_to(self, address, port):
        sock = socks.socksocket()
        sock.settimeout(60)
        sock.setproxy(socks.PROXY_TYPE_SOCKS5, "localhost", 9050, True)

        tor_controller = stem.control.Controller.from_port(port=9051)
        tor_controller.authenticate()
        tor_controller.new_circuit()

        Logger.get_logger().info(f"connecting to {address} port {port}")

        try:
            sock.connect((address, 80))
        except Exception as exc:
            Logger.get_logger().error(exc)

        Logger.get_logger().info(
            f"NodeConnection.send: Started with client ({address}) ':{str(port)}'"
        )

        self.create_new_connection(sock)

    def run(self):
        with Socket(self.network_manager.host, self.network_manager.port) as sock:
            while not self.terminate_flag.is_set():
                try:
                    conn, host = sock.accept()
                    new_connection = self.create_new_connection(conn)
                    self.network_manager.node_connections.append(new_connection)
                except socket.timeout:
                    continue
                except socket.error as exc:
                    if exc.errno == errno.ECONNRESET:
                        Logger.get_logger().error(f"SocketClosed: {str(exc)}")
                except Exception as exc:
                    Logger.get_logger().error(exc)
    def create_new_connection(self, conn):
        return NodeConnection(conn)
