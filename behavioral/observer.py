from __future__ import annotations
from typing import List


class Observable:
    """ Observable """

    def __init__(self):
        self.observers: List[Observer] = []

    def subscribe(self, observer: Observer):
        if observer not in self.observers:
            self.observers.append(observer)

    def notify(self, msg: str):
        for observer in self.observers:
            observer.notify(msg)


class Observer:
    """ Observer """

    def __init__(self, name: str):
        self.name = name

    def notify(self, msg: str):
        print(f'{self.name} got {msg}')


def main():
    observer1 = Observer('observer-1')
    observer2 = Observer('observer-2')

    observable = Observable()
    observable.subscribe(observer1)
    observable.subscribe(observer2)

    observable.notify('meeeessage')


if __name__ == '__main__':
    main()
