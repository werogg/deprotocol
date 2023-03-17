import socks

from logger.logger import Logger
from network.tor_network import TorService
from p2p import Node
from tor.tor_client import TorClient
import time
import socket

if __name__ == '__main__':
    logger = Logger('DeChat')
    tor_client = TorClient()
    tor_client.download_and_install()
    tor_service = TorService(9051)
    tor_service.start()
    new = Node('127.0.0.1', 65432)  # start the node
    new.start()

    socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5, '127.0.0.1', 9050)
    print("RUNNING IN CONSOLE MODE")
    try:
        while True:
            cmd = input("PYTHONP2P>")
            if cmd == "help":
                print(
                    """
                connect
                msg
                debug
                stop
                exit
                refresh
                add
                peers
                req
                load
                save
                """
                )
            if "connect " in cmd:
                args = cmd.replace("connect ", "")
                print("connect to: " + args)
                new.connect_to(args, 65432)

            if "msg " in cmd:
                args = cmd.replace("msg ", "")
                print("sent msg: " + args)
                new.message("msg", args)

            if cmd == "debug":
                new.debug = not new.debug
                print("Debug is now " + str(new.debug))

            if cmd == "stop":
                new.stop()

            if cmd == "exit":
                new.stop()
                exit(0)

            if cmd == "load":
                new.loadstate()

            if cmd == "save":
                new.savestate()

            if cmd == "refresh":
                new.file_manager.refresh()
                print(new.file_manager.files)

            if "add " in cmd:
                args = cmd.replace("add ", "")
                print("Adding file: " + args)
                try:
                    print(new.file_manager.addfile(args))
                    new.file_manager.refresh()
                except Exception as e:
                    print(e)

            if cmd == "peers":
                print("IP: " + new.ip)
                new.debug_print(new.peers)
                print("--------------")
                for i in new.nodes_connected:
                    print(
                        i.id
                        + " ("
                        + i.host
                        + ") - "
                        + str(time.time() - int(i.last_ping))
                        + "s"
                    )
                if len(new.peers) == 0:
                    print("NO PEERS CONNECTED")
                print("--------------")

            if "req " in cmd:
                args = cmd.replace("req ", "")
                print("requesting file with hash: " + args)
                new.requestFile(args)
    except Exception as e:
        new.stop()
        raise (e)
