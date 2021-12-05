import time
import threading
from concurrent.futures import ThreadPoolExecutor


def lprint(*args):
    """ Synchronized print """
    if not hasattr(lprint, 'lock'):
        lprint.lock = threading.Lock()

    with lprint.lock:
        print(*args)


def use_thread_local(i):
    # Create thread-local storage
    data = threading.local()

    # Set thread-local data
    setattr(data, str(i), i)

    # `setattr`does not affect thread-local storage each other.
    for _ in range(2):
        lprint(f'[Thread-{threading.get_native_id()}]', data.__dict__)
        time.sleep(0.5)


def main():
    fs = []
    with ThreadPoolExecutor() as executor:
        for i in range(5):
            fs.append(executor.submit(use_thread_local, i))

    for f in fs:
        f.result()


if __name__ == '__main__':
    main()
