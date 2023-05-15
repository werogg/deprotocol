import asyncio
import time

from application.logger.logger import Logger
from application.app.de_app import DeApp
from application.settings import NODE_PORT


class DeConsole:
    def __init__(self):
        self.app = None
        self.tor_service = None
        self.node = None
        self.terminate_flag = asyncio.Event()

    async def start(self, *args, **kwargs) -> None:

        def set_cls_vars() -> None:
            if args:
                self.app, self.tor_service, self.node = args
            Logger.get_instance().info("Console started correctly!")

        try:
            set_cls_vars()
        except Exception as exs:
            Logger.get_instance().error(exs)

        while not self.terminate_flag.is_set():
            try:

                await self.handle_console()

            except KeyboardInterrupt:
                Logger.get_instance().info("User requested stopping the protocol, stopping!")
                self.stop()

            # BUG: add exception for bug "Invalid protocol version"

            except Exception as exc:
                Logger.get_instance().info(f"An exception is stopping DeProtocol! ({exc})")
                self.stop()

        Logger.get_instance().info("DeProtocol successfully closed, see you soon!")

    def stop(self) -> None:
        self.terminate_flag.set()

    async def handle_console(self) -> None:

        async def async_input(prompt='') -> str:
            print(prompt, end='', flush=True)
            return (await asyncio.get_running_loop().run_in_executor(None, input)).rstrip('\n')

        cmd = await async_input("\nDEPROTO>")
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
            await self.node.connect(args, port=65432)

        if "msg " in cmd:
            args = cmd.replace("msg ", "")
            Logger.get_instance().info(f"Sent message: {args}")
            await self.node.message("msg", args)

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

    def print_peers(self) -> None:
        print(f"Address: {self.tor_service.get_address()}")
        print("--------------")
        for i in self.node.node_connections:
            print(
                i.id
                + " ("
                + i.connected_host
                + ") - "
                + str(time.time() - int(i.last_ping))
                + "s"
            )
        if len(self.node.node_connections) == 0:
            print("NO PEERS CONNECTED")
        print("--------------")