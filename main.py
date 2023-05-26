import asyncio
from application.app.application import DeProtocol
from application.utils.portforwardlib import forwardPort

if __name__ == '__main__':
    main_app = DeProtocol()
    asyncio.run(main_app.on_start())

