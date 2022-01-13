from abc import ABC, abstractmethod


class User:
    def __init__(self, role: str = 'user'):
        self.role = role


class DataManager(ABC):
    @abstractmethod
    def query(self):
        raise NotImplementedError


class UserDataManager(DataManager):
    def query(self):
        print('Query user data')


class AdminRequiredUserDataManager(DataManager):
    """ A proxy class of UserDataManager to restrict execution from non-admin users """

    def __init__(self, user: User):
        self.manager = UserDataManager()
        self.user = user

    def query(self):
        if self.user.role == 'admin':
            self.manager.query()
        else:
            print('Only admin can execute query.')


def main():
    user = User('user')
    admin = User('admin')

    UserDataManager().query()
    AdminRequiredUserDataManager(user).query()
    AdminRequiredUserDataManager(admin).query()


if __name__ == '__main__':
    main()
