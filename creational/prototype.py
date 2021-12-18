from __future__ import annotations
import copy


class Prototype:
    def __init__(self, name):
        self.name = name
        # there might be more expensive processes to initialize object

    def clone(self, name=None) -> Prototype:
        _clone = copy.deepcopy(self)  # or
        if name:
            _clone.name = name
        return _clone


def main():
    p = Prototype(name='foo')
    c = p.clone(name='bar')
    print(id(p), p.name)  # 139728967565264 foo
    print(id(c), c.name)  # 139728967562768 bar


if __name__ == '__main__':
    main()
