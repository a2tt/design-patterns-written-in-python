class DataBase:
    REGISTRY = {}

    def __new__(cls, type_):
        if type_ not in cls.REGISTRY.keys():
            cls.REGISTRY[type_] = object.__new__(cls)

        return cls.REGISTRY[type_]

    def connect(self):
        pass

    def query(self):
        pass


if __name__ == '__main__':
    mysql = DataBase('mysql')
    postgresql = DataBase('postgresql')
    print(DataBase.REGISTRY)  # {'mysql': <...>, 'postgresql': <...>'}
