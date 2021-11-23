class User:
    def __init__(self, uid, name):
        self.uid = uid
        self.name = name

    @staticmethod
    def send_email(content) -> bool:
        # ...
        print(f'Email sent\n{"-" * 10}\n> {content}\n{"-" * 10}')
        is_success = True
        return True if is_success else False


class NonUser(User):
    def __init__(self, *args):
        super().__init__(0, '')

    @staticmethod
    def send_email(*args):
        print('+No user data')
        return True


if __name__ == '__main__':
    users = [
        User(1, 'Kevin'),
        User(2, 'Martin'),
        NonUser(0, 'error'),
        User(4, 'Tom')
    ]

    for user in users:
        user.send_email(f'Hi {user.name}')
