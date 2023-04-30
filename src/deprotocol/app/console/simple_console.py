import threading
import time

from deprotocol.app.logger import Logger


class DeConsole(threading.Thread):

    def __init__(self, node, tor_service):
        super().__init__()
        self.node = node
        self.tor_service = tor_service
        self.terminate_flag = threading.Event()

    def run(self):
        while not self.terminate_flag.is_set():
            try:
                self.handle_console()
            except KeyboardInterrupt:
                Logger.get_logger().error("User requested stopping the protocol, stopping!")
                self.stop()
            except Exception as exc:
                Logger.get_logger().error(f"An exception is stopping DeProtocol! ({exc})")
                self.stop()
        Logger.get_logger().info("DeProtocol successfully closed, see you soon!")

    def stop(self):
        self.terminate_flag.set()

    def handle_console(self):
        cmd = input("\nDEPROTO>")
        if cmd == "help":
            print(
                """
                    connect
                    msg
                    stop
                    exit
                    peers
                    address
                    """
            )
        if "connect " in cmd:
            args = cmd.replace("connect ", "")
            self.node.connect_to(args, port=65432)

        if "msg " in cmd:
            args = cmd.replace("msg ", "")
            Logger.get_logger().info(f"Sent message: {args}")
            self.node.message("msg", args)

        if cmd == "stop":
            self.node.stop()
            self.terminate_flag.set()

        if cmd == "exit":
            self.node.stop()
            self.terminate_flag.set()

        if cmd == "load":
            self.node.loadstate()

        if cmd == "save":
            self.node.savestate()

        if cmd == "address":
            print(f"{self.tor_service.get_address()}.onion")

        if cmd == "peers":
            self.print_peers()

    def print_peers(self):
        print(f"Address: {self.tor_service.get_address()}")
        Logger.get_logger().info(self.node.peers)
        print("--------------")
        for i in self.node.nodes_connected:
            print(
                i.id
                + " ("
                + i.connected_host
                + ") - "
                + str(time.time() - int(i.last_ping))
                + "s"
            )
        if len(self.node.peers) == 0:
            print("NO PEERS CONNECTED")
        print("--------------")