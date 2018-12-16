from http.client import responses as http_response
from wsgiref.headers import Headers
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
            url_vars = matched.groupdict()
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
    def forms(self):
        form = cgi.FieldStorage(
            fp=self.environ['wsgi.input'],
            environ=self.environ,
            keep_blank_values=True,
        )
        params = {k: form[k].value for k in form}
        return params

    @property
    def query(self):
        return parse_qs(self.environ['QUERY_STRING'])

    @property
    def body(self):
        if self._body is None:
            content_length = int(self.environ.get('CONTENT_LENGTH', 0))
            self._body = self.environ['wsgi.input'].read(content_length)
            return self._body

    @property
    def text(self):
        return self.body.decode(self.charset)

    @property
    def json(self):
        return json.loads(self.body)



class Response:
    default_status = 200
    default_charset = 'utf-8'
    default_content_type = 'text/html; charser=UTF-8'

    def __init__(self, body='', status=None, headers=None, charset=None):
        self._body = body
        self.status = status or self.default_status
        self.headers = Headers()
        self.charset = charset or self.default_charset

        if headers:
            for name, value in headers.items():
                self.headers.add_header(name, value)

    @property
    def status_code(self):
        return "%d %s" % (self.status, http_response[self.status])

    @property
    def header_list(self):
        if 'Content-Type' not in self.headers:
            self.headers.add_header('Content-Type', self.default_content_type)
            return self.headers.items()

    @property
    def body(self):
        if isinstance(self._body, str):
            return [self._body.encode(self.charset)]
        return [self._body]


class JSONResponse(Response):
    default_content_type = 'text/json; charset=UTF-8'

    def __init__(self, dic, status=200, headers=None, charset=None, **dump_args):
        self.dic = dic
        self.json_dump_args = dump_args
        super().__init__('', status=status, headers=headers, charset=charset)

    @property
    def body(self):
        return [json.dumps(self.dic, **self.json_dump_args.encode(self.charset))]




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
        callback, url_vars = self.router.match(request.method, request.path)
        response = callback(request, **url_vars)
        start_response(response.status_code, response.header_list)
        return response.body

