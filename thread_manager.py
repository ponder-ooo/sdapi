
import threading
import queue
from terminal import logger

log = logger('manager')

def thread_manager(thread_manager_queue, worker_function, worker_args):
    log('running')

    worker_thread = None
    kill_event = threading.Event()

    while True:
        command = thread_manager_queue.get()

        if command == 'launch':
            log('launching worker')
            if worker_thread is not None:
                log('worker already running. send "reset" signal to re-launch')
                continue
            worker_thread = threading.Thread(target=worker_function, args=(kill_event,)+worker_args)
            worker_thread.start()
            continue

        if command == 'exit':
            log('exiting')
            if worker_thread is not None:
                kill_event.set()
                worker_thread.join()
            return

        if command == 'reset':
            log('re-launching worker')
            if worker_thread is not None:
                kill_event.set()
                worker_thread.join()
                kill_event.clear()
            worker_thread = threading.Thread(target=worker_function, args=(kill_event,)+worker_args)
            worker_thread.start()
            continue

        log(f'unknown command "{command}"')


def launch(target, args):
    thread = threading.Thread(target=target, args=args)
    thread.start()
    return thread

