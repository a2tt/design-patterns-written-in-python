import time
import threading
from typing import Any, Iterable
from collections import deque


class Queue:
    def __init__(self):
        self.mutex = threading.Lock()
        self.condition = threading.Condition(self.mutex)
        self.queue = deque()

    @property
    def is_empty(self) -> bool:
        return len(self.queue) == 0

    def get(self):
        with self.condition:
            # If nothing is in the queue, wait (guarded state)
            while self.is_empty:
                self.condition.wait()
            # You can use self.condition.wait_for method instead of while + wait

        return self.queue.popleft()

    def put(self, item: Any):
        with self.condition:
            self.queue.append(item)
            # Wake up condition-waiting thread after enqueue
            self.condition.notify()


def lprint(*args: Iterable):
    """ synchronized print """
    if not hasattr(lprint, 'lock'):
        lprint.lock = threading.Lock()

    with lprint.lock:
        print(*args)


def producer(q: Queue):
    for i in range(5):
        time.sleep(0.5 * i)
        item = i ** 2
        lprint(f'Producer put {item}')
        q.put(item)


def consumer(q: Queue):
    for i in range(3):
        item = q.get()
        lprint(f'Consumer get {item}')


def main():
    q = Queue()

    consumer_thr = threading.Thread(target=consumer, args=(q,))
    producer_thr = threading.Thread(target=producer, args=(q,))

    consumer_thr.start()
    producer_thr.start()


if __name__ == '__main__':
    main()
