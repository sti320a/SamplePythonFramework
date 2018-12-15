import re


def http404(env, start_response):
    start_response('404 Not Found', [('Content-type', 'text/plain; charset=utf-8')])
    return [b'404 Not Found']

def http405(env, start_response):
    start_response('405 Method Not Allowed', [('Content-type', 'text/plain; charset=utf-8')])
    return [b'405 Method Not Allowed']


class Router:
    def __init__(self):
        self.routes = []

    def add(self, method, path, callback):
        self.routes.append({
            'method': method,
            'path': '^'+path+'$',
            'path_compiled': re.compile('^'+path+'$'),
            'callback': callback
        })

    def match(self, method, path):
        error_callback = http404
        for rts in self.routes:
            matched = rts['path_compiled'].match(path)
            if not matched:
                continue
            error_callback = http405
            print('method: {}'.format(method))
            url_vars = matched.groupdict()
            print('url_vars: {}'.format(url_vars))
            print('matched_goupdict: {}'.format(matched.groupdict))
            if method == rts['method']:
                return rts['callback'], url_vars
        return error_callback, {}


class Request:
    def __init__(self, environ):
        self.environ = environ
        self._body = None
    
    @property
    def path(self):
        return self.environ['PATH_INFO'] or '/'
    
    @property
    def method(self):
        return self.environ['REQUEST_METHOD'].upper()

    @property
    def body(self):
        if self._body is None:
            content_length = int(self.environ.get('CONTENT_LENGTH', 0))
            self._body = self.environ['wsgi.input'].read(content_length)
            return self._body

class App:
    def __init__(self):
        self.router = Router()

    def route(self, path=None, method='GET', callback=None):
        def decorator(callback_func):
            self.router.add(method, path, callback_func)
            return callback_func
        return decorator(callback) if callback else decorator

    def __call__(self, env, start_response):
        request = Request(env)
        callback, kwargs = self.router.match(request.method, request.path)
        return callback(env, start_response, **kwargs)

