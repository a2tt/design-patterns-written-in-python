from __future__ import annotations
from typing import List


class Observer:
    def __init__(self, name: str):
        self.name = name
        self.observers: List[Observer] = []
        self.blocked_observers: List[Observer] = []  # Do not notify to these observers

    def subscribe(self, observer: Observer):
        if observer not in self.observers:
            self.observers.append(observer)

    def add_blocked_observer(self, observer: Observer):
        if observer not in self.blocked_observers:
            self.blocked_observers.append(observer)

    def remove_blocked_observer(self, observer: Observer):
        if observer in self.blocked_observers:
            self.blocked_observers.append(observer)

    def notify(self):
        """ Send notification to observers """
        print(f'[{self.name}] Notify to {self.observers}')
        for observer in self.observers:
            observer.notified(self)

    def notified(self, sender: Observer):
        """ notified """
        # Prevent mutual invocation
        if sender in self.blocked_observers:
            return
        self.add_blocked_observer(sender)

        # Otherwise, infinite loop can occur when this object subscribes one of the subscribers.
        print(f'[{self.name}] Notified by {sender.name}')
        self.notify()

        # Resume blocked observer
        self.remove_blocked_observer(sender)

    def __repr__(self):
        return f'Observer({self.name})'


def main():
    obj1 = Observer('obj1')
    obj2 = Observer('obj2')
    obj3 = Observer('obj3')

    obj1.subscribe(obj2)
    obj2.subscribe(obj3)
    obj3.subscribe(obj1)

    obj1.notify()


if __name__ == '__main__':
    main()
