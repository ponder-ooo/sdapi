
import asyncio
from websockets.server import serve
from server.server import setup
from util.terminal import logger

log = logger('main')

async def main(server):
    server = await serve(server, "localhost", 8765)
    log("websocket server running on localhost:8765");
    try:
        await asyncio.Future()
    except (KeyboardInterrupt, asyncio.CancelledError):
        print('\n')
        log('Keyboard Interrupt. Exiting.')
    finally:
        server.close()
        await server.wait_closed()

if __name__ == '__main__':
    server, cleanup = setup()

    asyncio.run(main(server))

    cleanup()

