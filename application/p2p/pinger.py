import asyncio

from application.logger.logger import Logger


class Pinger:

    def __init__(self, parent):
        self.terminate_flag = asyncio.Event()
        self.parent = parent
        self.dead_time = 30  # time to disconect from node if not pinged

    def stop(self):
        self.terminate_flag.set()

    async def start(self):
        Logger.get_instance().info("Pinger Started")
        while not self.terminate_flag.is_set():
            for node_ in self.parent.node_connections:
                await node_.send("ping")
                await asyncio.sleep(20)
        Logger.get_instance().info("Pinger stopped")



