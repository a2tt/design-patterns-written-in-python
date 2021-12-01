from enum import Enum
from typing import Any
from concurrent.futures import ThreadPoolExecutor
import threading


class PrinterState(Enum):
    PRINTING = 1
    STANDBY = 2


class Printer:
    lock = threading.Lock()

    def __init__(self):
        self.state = PrinterState.STANDBY

    def print(self, content: Any):
        with self.lock:
            # if printer in PRINTING state, return
            if self.state == PrinterState.PRINTING:
                return
            self.state = PrinterState.PRINTING

        print(content)
        self.state = PrinterState.STANDBY


def main():
    printer = Printer()
    with ThreadPoolExecutor(max_workers=4) as executor:
        for i in range(0, 50):
            executor.submit(printer.print, i)


if __name__ == '__main__':
    main()
