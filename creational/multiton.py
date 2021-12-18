class DataBase:
    REGISTRY = {}

    def __new__(cls, type_):
        """
        Instantiate the multiton class when `type_` has never been used to
        created and return the object.
        """
        # Thread-safe operations required (ex. lock)
        if type_ not in cls.REGISTRY.keys():
            cls.REGISTRY[type_] = object.__new__(cls)

        return cls.REGISTRY[type_]

    def connect(self):
        pass

    def query(self):
        pass


def main():
    mysql = DataBase('mysql')
    postgresql = DataBase('postgresql')
    print(DataBase.REGISTRY)  # {'mysql': <...>, 'postgresql': <...>'}


if __name__ == '__main__':
    main()
