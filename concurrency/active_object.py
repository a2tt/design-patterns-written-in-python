import string
import time
import random
from concurrent.futures import ThreadPoolExecutor, wait
from queue import Queue
from threading import Thread
from typing import Any


class Websocket:
    """ Execution class """

    def __init__(self):
        self.run = True
        self.queue = Queue()  # List of pending requests
        self.run_forever_thr = Thread(target=self.run_forever)
        self.run_forever_thr.start()

    def run_forever(self):
        """ Scheduler can implement other scheduling policies """
        print('Start run_forever')
        while self.run:
            msg = self.queue.get()
            print(f'Send : {msg}')
            time.sleep(random.random())

    def enqueue_item(self, item: str):
        if self.run:
            self.queue.put(item)

    def stop(self):
        self.run = False


class Client:
    """ Invocation class """

    def __init__(self, name: str, ws: Websocket):
        self.name = name
        self.ws = ws

    def send_random_msg(self, prefix: Any):
        msg = f'[{self.name}] {prefix}-{"".join(random.sample(string.ascii_letters, 6))}'
        self.ws.enqueue_item(msg)


def main():
    ws = Websocket()

    client_1 = Client('c1', ws)
    client_2 = Client('c2', ws)

    # call `Client.send_random_msg` asynchronously
    fs = []
    with ThreadPoolExecutor() as executor:
        for i in range(0, 10):
            fs.extend([
                executor.submit(client_1.send_random_msg, i),
                executor.submit(client_2.send_random_msg, i),
            ])

    # wait until all messages are sent
    wait(fs)

    # stop thread
    ws.stop()


if __name__ == '__main__':
    main()
