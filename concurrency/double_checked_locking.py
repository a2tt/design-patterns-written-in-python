from concurrent.futures import ThreadPoolExecutor
import threading


class Logger:
    _instance = None
    _lock = threading.Lock()
    _log_lock = threading.Lock()

    def __new__(cls):
        # To reduce the overhead of acquiring a lock, check `_instance` first
        if not cls._instance:
            # If `_instance` is not initialized, then acquire a lock
            with cls._lock:
                if not cls._instance:
                    cls._instance = object.__new__(cls)

        return cls._instance

    def log(self, *args):
        with self._log_lock:
            print(*args)


def create_logger():
    log = Logger()
    log.log(f'[{threading.get_ident()}] Logger({id(log)}) initiated')


def main():
    with ThreadPoolExecutor() as executor:
        for _ in range(10):
            executor.submit(create_logger)


if __name__ == '__main__':
    main()
