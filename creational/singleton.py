import threading


class Logger:
    _instance = None
    _lock = threading.Lock()

    def __new__(cls):
        with cls._lock:
            if not cls._instance:
                cls._instance = object.__new__(cls)

        return cls._instance

    def log(self, *args):
        pass


if __name__ == '__main__':
    log = Logger()
    log.log('text')
