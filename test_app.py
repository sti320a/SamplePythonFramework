from app import App, Response, JSONResponse
from wsgiref.simple_server import make_server

app = App()

@app.route('/(?P<name>\w+)', 'GET')
def hello(request, name): 
    return JSONResponse({'foo':'bar'})

@app.route('/night', 'GET')
def goodnight(request):
    return Response('Hello World')

if __name__ == '__main__':
    httpd = make_server('', 8000, app)
    httpd.serve_forever()