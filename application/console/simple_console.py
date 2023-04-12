import time


def read_user_input(new, tor_service):
    try:
        while True:
            cmd = input("\nDEPROTO>")
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
                address
                """
                )
            if "connect " in cmd:
                args = cmd.replace("connect ", "")

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

            if cmd == "address":
                print(f"{tor_service.get_address()}.onion")

            if "add " in cmd:
                args = cmd.replace("add ", "")
                print("Adding file: " + args)
                try:
                    print(new.file_manager.addfile(args))
                    new.file_manager.refresh()
                except Exception as e:
                    print(e)

            if cmd == "peers":
                print("Address: " + tor_service.get_address())
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