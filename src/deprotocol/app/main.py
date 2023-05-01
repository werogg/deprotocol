from deprotocol.app.application import DeProtocol


def main():
    deprotocol = DeProtocol()

    try:
        deprotocol.on_start()
    except (KeyboardInterrupt, Exception):
        deprotocol.on_stop()


if __name__ == '__main__':
    main()
