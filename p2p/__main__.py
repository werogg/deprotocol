import socks

import stem
import socket
from network.tor_network import TorService
from p2p.node import *


if __name__ == "__main__":
    new = Node("", PORT, FILE_PORT)  # start the node
    new.start()

    socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5, '127.0.0.1', 9050)

    # create a new socket object
    s = socks.socksocket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(10)

    tor_controller = stem.control.Controller.from_port(port=9051)
    tor_controller.authenticate()

    circuit = tor_controller.new_circuit()
    #tor_controller.get_circuit(circuit)

    #socket.socket = socks.socksocket
    #sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Connect the socket to the hidden service via the Tor circuit
    s.connect(('fsahlvmebwlqcaqmv7poqz7q3rg2u3dsqmhg4zbpj4ddjfqikk65f2qd.onion', 80))

    s.send(b'test')
    response = s.recv(1024)
    print(response)


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
                new.connect_to(args, PORT)

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
