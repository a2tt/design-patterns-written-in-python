import random
import time
import threading
import queue

from typing import Union


class Connection:
    def __init__(self):
        # establish connection, and so on.
        pass

    def clear(self, *args):
        """ clear self instance for next usage """

    def query(self, *args):
        """ execute query """
        time.sleep(random.randint(0, 2))


class ConnectionPool:
    POOL = queue.Queue()

    def __init__(self):
        self._connection: Union[Connection, None] = None

    def __enter__(self):
        if ConnectionPool.POOL.empty():
            ConnectionPool.POOL.put(Connection())

        self._connection = ConnectionPool.POOL.get()
        return self._connection

    def __exit__(self, Type, value, traceback):
        ConnectionPool.POOL.put(self._connection)
        self._connection.clear()
        self._connection = None


def main():
    with ConnectionPool() as conn:
        conn.query()


if __name__ == '__main__':
    thrs = []
    for i in range(10):
        thrs.append(threading.Thread(target=main))

    for thr in thrs:
        thr.start()
