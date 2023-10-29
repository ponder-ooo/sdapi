
import asyncio
import json
import threading
import queue
from websockets.server import serve
from sd.sd import main as sd_main
from .thread_manager import launch, thread_manager
import concurrent.futures
from util.terminal import logger

log = logger('server')

def setup():
    log('setup')

    thread_manager_queue = queue.Queue()
    sd_command_queue = queue.Queue()
    sd_response_queue = queue.Queue()

    manager_thread = launch(thread_manager, (thread_manager_queue, sd_main, (sd_command_queue, sd_response_queue)))

    thread_manager_queue.put('launch')

    def cleanup():
        log('cleanup')
        thread_manager_queue.put('exit')
        manager_thread.join()

    async def response_loop(websocket):
        while True:
            if not sd_response_queue.empty():
                response = sd_response_queue.get()
                await websocket.send(response)
            await asyncio.sleep(0.1)

    async def socket_server(websocket):
        response_task = asyncio.create_task(response_loop(websocket))

        async for message in websocket:
            if (message == ''):
                log('received empty signal')
                continue

            decoded = json.loads(message)

            if isinstance(decoded, str):
                await websocket.send(f"[str] received: {decoded}")
                continue

            if isinstance(decoded, dict):
                if 'command' in decoded:
                    sd_command_queue.put(decoded)
                else:
                    await websocket.send(f"[dict] received")
                continue

            log('unhandled signal of type {type(decoded)}')

        response_task.cancel()

    return socket_server, cleanup

