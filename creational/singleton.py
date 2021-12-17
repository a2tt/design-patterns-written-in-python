import threading


class Logger:
    _instance = None
    _lock = threading.Lock()

    def __new__(cls):
        """ Instantiate the singleton class if not created yet and return the object. """
        with cls._lock:  # Prevent simultaneous instantiation in a multi threaded environment.
            if not cls._instance:
                cls._instance = object.__new__(cls)

        return cls._instance

    def log(self, *args):
        print(*args)


def main():
    log = Logger()
    log.log('text')


if __name__ == '__main__':
    main()
