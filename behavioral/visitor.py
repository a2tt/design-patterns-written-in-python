from __future__ import annotations
from abc import ABC, abstractmethod
from typing import List


class Element(ABC):
    def __init__(self):
        self.children: List[Element] = []

    @abstractmethod
    def accept(self, visitor: Visitor):
        for child in self.children:
            child.accept(visitor)

    def add_child(self, element: Element):
        self.children.append(element)


class A(Element):
    def accept(self, visitor: Visitor):
        super().accept(visitor)
        visitor.visit_a(self)


class B(Element):
    def accept(self, visitor: Visitor):
        super().accept(visitor)
        visitor.visit_b(self)


class Visitor(ABC):
    @abstractmethod
    def visit_a(self, element: Element):
        raise NotImplementedError

    @abstractmethod
    def visit_b(self, element: Element):
        raise NotImplementedError


class PrintVisitor(Visitor):
    def visit_a(self, element: Element):
        print('Visit A', element)

    def visit_b(self, element: Element):
        print('Visit B', element)


class LogVisitor(Visitor):
    def visit_a(self, element: Element):
        print('Log A', element)

    def visit_b(self, element: Element):
        print('Log B', element)


def main():
    a = A()
    a.accept(PrintVisitor())
    a.accept(LogVisitor())

    b = B()
    b.add_child(a)
    b.accept(PrintVisitor())
    b.accept(LogVisitor())


if __name__ == '__main__':
    main()
