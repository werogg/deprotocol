import socket
import sys
import threading
import time

import socks

from application.utils import crypto_funcs as cf


class NodeConnection(threading.Thread):
    def __init__(self, main_node, sock, id, host, port):

        super(NodeConnection, self).__init__()
        socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5, '127.0.0.1', 9050)

        self.host = host
        self.port = port
        self.main_node = main_node
        self.sock = sock
        self.terminate_flag = threading.Event()
        self.last_ping = time.time()
        # Variable for parsing the incoming json messages
        self.buffer = ""

        # The id of the connected node
        self.public_key = cf.load_key(id)
        self.id = id

        self.main_node.debug_print(
            "NodeConnection.send: Started with client ("
            + self.host
            + ") '"
            + ":"
            + str(self.port)
            + "'"
        )

    def send(self, data):

        try:
            data = f"{data}-TSN"
            self.sock.sendall(data.encode("utf-8"))

        except Exception as e:
            self.main_node.debug_print(
                "NodeConnection.send: Unexpected ercontent/ror:"
                + str(sys.exc_info()[0])
            )
            self.main_node.debug_print(f"Exception: {str(e)}")
            self.terminate_flag.set()

    def stop(self):
        self.terminate_flag.set()

    def run(self):
        self.sock.settimeout(10.0)

        while not self.terminate_flag.is_set():
            if time.time() - self.last_ping > self.main_node.dead_time:
                self.terminate_flag.set()
                print(f"node{self.id}is dead")

            line = ""

            try:
                line = self.sock.recv(4096)

            except socket.timeout:
                # self.main_node.debug_print("NodeConnection: timeout")
                pass

            except Exception as e:
                self.terminate_flag.set()
                self.main_node.debug_print(
                    f"NodeConnection: Socket has been terminated ({line})"
                )
                self.main_node.debug_print(e)

            if line != "":
                try:
                    # BUG: possible buffer overflow when no -TSN is found!
                    self.buffer += str(line.decode("utf-8"))

                except Exception as e:
                    print(f"NodeConnection: Decoding line error | {str(e)}")

                # Get the messages by finding the message ending -TSN
                index = self.buffer.find("-TSN")
                while index > 0:
                    message = self.buffer[:index]
                    self.buffer = self.buffer[index + 4::]

                    if message == "ping":
                        self.last_ping = time.time()
                        # self.main_node.debug_print("ping from " + self.id)
                    else:
                        self.main_node.node_message(self, message)

                    index = self.buffer.find("-TSN")

            time.sleep(0.01)

        self.main_node.node_disconnected(self)
        self.sock.settimeout(None)
        self.sock.close()
        del self.main_node.nodes_connected[self.main_node.nodes_connected.index(self)]
        time.sleep(1)
