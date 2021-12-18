"""
RAII(Resource-Acquisition-Is-Initialization) is not available on garbage collected languages like python.
There should be scope-based deterministic destruction.

In python, there is `with` statement. But it is not with RAII idiom.
"""


def main():
    # using `with`, __enter__ and __exit__ methods are executed no matter what happens.
    with open('test.log', 'wt') as fp:
        pass

    # but variable `fp` still there
    print(fp)


if __name__ == '__main__':
    main()
