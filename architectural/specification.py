from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Any


class BaseSpecification(ABC):
    @abstractmethod
    def is_satisfied_by(self, candidate: Any) -> bool:
        raise NotImplementedError

    def __call__(self, candidate: Any) -> bool:
        return self.is_satisfied_by(candidate)

    def __and__(self, other: BaseSpecification) -> AndSpecification:
        return AndSpecification(self, other)

    def __or__(self, other: BaseSpecification) -> OrSpecification:
        return OrSpecification(self, other)

    def __neg__(self, other: BaseSpecification) -> NotSpecification:
        return NotSpecification(self)


class AndSpecification(BaseSpecification):
    def __init__(self, first: BaseSpecification, second: BaseSpecification):
        self.first = first
        self.second = second

    def is_satisfied_by(self, candidate: Any) -> bool:
        return self.first.is_satisfied_by(candidate) and self.second.is_satisfied_by(candidate)


class OrSpecification(BaseSpecification):
    def __init__(self, first: BaseSpecification, second: BaseSpecification):
        self.first = first
        self.second = second

    def is_satisfied_by(self, candidate: Any) -> bool:
        return self.first.is_satisfied_by(candidate) or self.second.is_satisfied_by(candidate)


class NotSpecification(BaseSpecification):
    def __init__(self, subject: BaseSpecification):
        self.subject = subject

    def is_satisfied_by(self, candidate: Any) -> bool:
        return not self.subject.is_satisfied_by(candidate)


class User:
    def __init__(self, level: int = 1):
        self.level = level


class UserSpecification(BaseSpecification):
    def is_satisfied_by(self, candidate: Any) -> bool:
        return isinstance(candidate, User)


class LevelLimitSpecification(BaseSpecification):
    def __init__(self, level_thres: int):
        self.level_thres = level_thres

    def is_satisfied_by(self, candidate: User) -> bool:
        return candidate.level >= self.level_thres


if __name__ == '__main__':
    non_user = 'non_user'
    u1 = User(1)
    u2 = User(50)

    print((UserSpecification() & LevelLimitSpecification(10)).is_satisfied_by(non_user))  # False
    print((UserSpecification() & LevelLimitSpecification(10)).is_satisfied_by(u1))  # False
    print((UserSpecification() & LevelLimitSpecification(10)).is_satisfied_by(u2))  # TRue
    print((UserSpecification() & LevelLimitSpecification(100)).is_satisfied_by(u2))  # False
    print((UserSpecification() | LevelLimitSpecification(1)).is_satisfied_by(u1))  # True
