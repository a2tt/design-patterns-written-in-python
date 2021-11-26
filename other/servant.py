from __future__ import annotations
from abc import ABC, abstractmethod


class Servant:
    """
    Servant
    Instead of defining `add_time` to TimeUtil interface, use Servant class to add time.
    """

    @staticmethod
    def add_time(service: TimeUtil, value: int):
        value += service.time
        service.modify_time_set(value)


class TimeUtil(ABC):
    """ Service """

    def __init__(self, time_set: float = 0):
        self.time = time_set

    @abstractmethod
    def modify_time_set(self, value: int):
        raise NotImplementedError('Please implement this abstract function.')

    def print(self):
        print(f'Time set: {self.time}')


class Timer(TimeUtil):
    """ The remaining time is reduced. """

    def modify_time_set(self, value: int):
        self.time = value
        self.print()

    def print(self):
        print(f'Timer | Time left: {self.time}')


class Stopwatch(TimeUtil):
    """ Time is ticking. """

    def modify_time_set(self, value: int):
        self.time = value
        self.print()

    def print(self):
        print(f'Stopwatch | Timed: {self.time}')


if __name__ == '__main__':
    timer = Timer(100)
    stopwatch = Stopwatch(0)

    timer.print()
    stopwatch.print()

    Servant.add_time(timer, 10)
    Servant.add_time(stopwatch, 10)
