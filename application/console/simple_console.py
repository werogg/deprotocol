import time

from application.logger.logger import Logger


def read_user_input(new, tor_service):
    try:
        while True:
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
                new.connect_to(args, port=65432)

            if "msg " in cmd:
                args = cmd.replace("msg ", "")
                Logger.get_instance().info(f"sent msg: {args}")
                new.message("msg", args)

            if cmd == "stop":
                new.stop()

            if cmd == "exit":
                new.stop()
                exit(0)

            if cmd == "load":
                new.loadstate()

            if cmd == "save":
                new.savestate()

            if cmd == "address":
                print(f"{tor_service.get_address()}.onion")

            if cmd == "peers":
                print(f"Address: {tor_service.get_address()}")
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
    except Exception as e:
        new.stop()
        raise (e)