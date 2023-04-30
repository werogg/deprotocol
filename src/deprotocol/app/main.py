import signal

from deprotocol.app.application import DeProtocol


def main():
    deprotocol = DeProtocol()

    signal.signal(signal.SIGINT, deprotocol.on_stop)
    signal.signal(signal.SIGTERM, deprotocol.on_stop)

    try:
        deprotocol.on_start()
    except (KeyboardInterrupt, Exception):
        deprotocol.on_stop()


if __name__ == '__main__':
    main()
