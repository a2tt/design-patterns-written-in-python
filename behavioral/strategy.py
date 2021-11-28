import bisect

from abc import ABC, abstractmethod
from typing import List


class Strategy(ABC):
    @abstractmethod
    def find_idx(self, items, target: int) -> int:
        raise NotImplementedError


class SequentialStrategy(Strategy):
    def find_idx(self, items, target: int) -> int:
        for idx, item in enumerate(items):
            if item == target:
                return idx
        return -1


class BinarySearchStrategy(Strategy):
    def find_idx(self, items, target: int) -> int:
        idx = bisect.bisect_left(items, target)
        if idx != len(items) and items[idx] == target:
            return idx
        return -1


class Searcher:
    def __init__(self, items: List[int], strategy: Strategy):
        self.items = items
        self.strategy = strategy

    def set_strategy(self, strategy: Strategy):
        self.strategy = strategy

    def find_idx(self, target: int) -> int:
        print(f'Find {target} from list using {self.strategy.__class__.__name__}')
        return self.strategy.find_idx(self.items, target)


def main():
    tests = [
        [1, 7, 4, 9, 10, -1, -3, 2],
        [-3, -1, 1, 2, 4, 7, 9, 10]
    ]

    for items in tests:
        is_sorted = sorted(items) == items
        strategy = BinarySearchStrategy if is_sorted else SequentialStrategy
        searcher = Searcher(items, strategy())
        print(searcher.find_idx(2))


if __name__ == '__main__':
    main()
