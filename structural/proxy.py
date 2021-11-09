from abc import ABC, abstractmethod


class User:
    def __init__(self, role: str = 'user'):
        self.role = role


class ABSPrivateDataManager(ABC):
    @abstractmethod
    def query(self):
        raise NotImplementedError


class PrivateDataManager:
    def query(self):
        print('Query user data')


class AdminRequiredPrivateDataManager(ABSPrivateDataManager):
    """ A proxy class of PrivateDataManager to restrict execution of non-admin users """

    def __init__(self, user: User):
        self.manager = PrivateDataManager()
        self.user = user

    def query(self):
        if self.user.role == 'admin':
            self.manager.query()
        else:
            print('Only admin can execute query.')


if __name__ == '__main__':
    user = User('user')
    admin = User('admin')

    PrivateDataManager().query()
    AdminRequiredPrivateDataManager(user).query()
    AdminRequiredPrivateDataManager(admin).query()
