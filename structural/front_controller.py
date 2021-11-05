import functools
from typing import Optional, List, Callable


class Request:
    def __init__(self, path: str = '/', method: str = 'GET'):
        self.path = path
        self.method = method


class Dispatcher:
    router_map = {}

    @classmethod
    def dispatch(cls, path: str, method: str):
        try:
            return cls.router_map.get((path, method))()
        except AttributeError:
            raise Exception('404 not found')

    @classmethod
    def route(cls, path: str, methods: Optional[List[str]] = None):
        def decorated(func: Callable):
            @functools.wraps(func)
            def _decorated(*args, **kwargs):
                return func(*args, **kwargs)

            for method in methods:
                cls.router_map[(path, method)] = _decorated
            return _decorated

        return decorated


class FrontController:
    def __init__(self):
        pass

    def dispatch(self, request: Request):
        Dispatcher.dispatch(request.path, request.method)


@Dispatcher.route('/', ['GET'])
def index():
    print('index')


@Dispatcher.route('/about', ['GET', 'POST'])
def about():
    print('I am a2tt!')


if __name__ == '__main__':
    FrontController().dispatch(Request('/', 'GET'))
    FrontController().dispatch(Request('/about', 'GET'))
    FrontController().dispatch(Request('/about', 'POST'))
