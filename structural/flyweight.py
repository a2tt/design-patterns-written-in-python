import random


class Badge:
    NAME = 'normal'


class VIPBadge(Badge):
    NAME = 'VIP'


class MVPBadge(Badge):
    NAME = 'MVP'


class BadgeFactory:
    _BADGES = {}

    @classmethod
    def get_badge(cls, type_: str) -> Badge:
        if type_ in cls._BADGES:
            return cls._BADGES[type_]

        if type_ == VIPBadge.NAME:
            cls._BADGES[type_] = VIPBadge()
        elif type_ == MVPBadge.NAME:
            cls._BADGES[type_] = MVPBadge()
        else:
            cls._BADGES[type_] = Badge()

        return cls._BADGES[type_]


class User:
    def __init__(self, name: str, badge: str = 'normal'):
        self.name = name
        self.badge = BadgeFactory.get_badge(badge)

    def introduce(self):
        print(f'My name is {self.name} and I have {self.badge.NAME}({id(self.badge)}) badge')


def main():
    users = []
    for i in range(0, 100):
        users.append(User(str(i), random.choice(['normal', VIPBadge.NAME, MVPBadge.NAME])))

    for user in users:
        user.introduce()


if __name__ == '__main__':
    main()
