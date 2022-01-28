"""
Python itself already implements the iterator pattern.
"""


class Counter:
    """ Custom iterator """

    def __init__(self, start: int, end: int):
        self.num = start - 1
        self.end = end

    def __iter__(self):
        return self

    def __next__(self):
        if self.num < self.end:
            self.num += 1
            return self.num

        raise StopIteration


def counter(start: int, end: int):
    """ Built-in generator """

    for c in range(start, end + 1):
        yield c


def main():
    for c in Counter(2, 5):
        print(c)

    for c in counter(6, 10):
        print(c)


if __name__ == '__main__':
    main()
