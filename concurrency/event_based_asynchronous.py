""" Referred to concurrent.futures.thread and concurrent.futures._base """

import itertools
import queue
import time
import threading
from typing import Iterable, Union, Callable, Any


def lprint(*args, **kwargs):
    if not hasattr(lprint, 'print_lock'):
        lprint.print_lock = threading.Lock()

    with lprint.print_lock:
        print(*args, **kwargs)


class _WorkItem:
    def __init__(self, fn: Callable, callback: Callable, args: Iterable, kwargs: dict):
        self.fn = fn
        self.callback = callback
        self.args = args
        self.kwargs = kwargs

    def run(self):
        res = self.fn(*self.args, **self.kwargs)
        if callable(self.callback):
            self.callback(res)


class Executor:
    _counter = itertools.count().__next__

    def __init__(self, max_worker: int = None):
        self.max_worker = max_worker or 4
        self._work_queue = queue.SimpleQueue()
        self._threads = set()
        self.lock = threading.Lock()
        self._shutdown = False

    def submit(self, fn: Callable, callback: Callable, *args, **kwargs):
        """ Make a reservation to call `fn` with `callback` """
        with self.lock:
            work = _WorkItem(fn, callback, args, kwargs)
            name = f'[Thread-Exe({self._counter()})]'
            self._work_queue.put(work)
            self._spawn_executor(name)

    def _spawn_executor(self, name: str):
        if len(self._threads) < self.max_worker:
            thr = threading.Thread(target=self._executor, name=name)
            thr.start()
            self._threads.add(thr)

    def _executor(self):
        while True:
            work: Union[_WorkItem, None] = self._work_queue.get(block=True)
            if work is not None:
                work.run()
                continue

            if self._shutdown:
                # Notify other executors too
                self._work_queue.put(None)
                break

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        with self.lock:
            self._shutdown = True

            # Wake up executor
            self._work_queue.put(None)
            for thr in self._threads:
                thr.join()

        return False


def sum_of_pow(num):
    """ Time consuming process """
    sum = 0
    start = time.time()
    for i in range(pow(num, num) + 1):
        sum += i
        time.sleep(0.01)

    res = round(time.time() - start, 4), sum
    return res


def callback(res: Any):
    lprint('Result: ', res)


def main():
    # Implemented `callback` instead of `Future`
    with Executor() as executor:
        for num in [2, 4, 3, 1]:
            executor.submit(sum_of_pow, callback, num)


if __name__ == '__main__':
    main()
