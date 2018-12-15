from app import App
from wsgiref.simple_server import make_server

app = App()

@app.route('/', 'GET')
# TODO:  request / start_responseの引数を入力不要に
def hello(request, start_response): 
    start_response('200 OK', [('Content-type', 'text/plain; charset=utf-8')])
    # encodeを不要にしたい
    return ['Hello World'.encode("utf-8")]

@app.route('/night', 'GET')
def goodnight(request, start_response):
    start_response('200 OK', [('Content-type', 'text/plain; charset=utf-8')])
    return ['Good night'.encode("utf-8")]


if __name__ == '__main__':
    httpd = make_server('', 8000, app)
    httpd.serve_forever()