
from queue import Empty
from terminal import logger

log = logger('sd')

def main(kill_event, command_queue, response_queue):
    log('running')
    while not kill_event.is_set():
        try:
            command = command_queue.get(timeout=1)
            process_command(command, response_queue)
        except Empty:
            pass
        except Exception as e:
            log(f'exception: {e}')
    log('exiting')


def process_command(command, response_queue):
    log(f'processing "{command["command"]}"')
    response_queue.put('fooooo')

