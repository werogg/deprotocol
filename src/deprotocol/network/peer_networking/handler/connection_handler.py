import errno
import socket
import threading

import socks
import stem

from deprotocol.event.events.deprotocol_ready_event import DeProtocolReadyEvent
from deprotocol.app.logger import Logger
from deprotocol.network.peer_networking.node_connection import NodeConnection
from deprotocol.network.peer_networking.proxied_socket import Socket


class ConnectionHandler(threading.Thread):
    def __init__(self, deprotocol, network_manager):
        super().__init__()
        self.deprotocol = deprotocol
        self.network_manager = network_manager
        self.terminate_flag = threading.Event()

        event = DeProtocolReadyEvent()
        self.deprotocol.listeners.fire(event)

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

        return self.create_new_connection(self.deprotocol, sock).start()

    def run(self):
        with Socket(self.network_manager.host, self.network_manager.port) as sock:
            while not self.terminate_flag.is_set():
                try:
                    conn, host = sock.accept()
                    Logger.get_logger().info("Connection created with a client1.")
                    new_connection = self.create_new_connection(self.deprotocol, conn)
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

    def create_new_connection(self, deprotocol, conn):
        return NodeConnection(deprotocol, conn, len(self.network_manager.node_connections))

    def stop(self):
        self.close_all_connections()
        self.terminate_flag.set()

    def close_all_connections(self):
        for conn in self.network_manager.node_connections:
            if conn:
                conn.stop()
