from app import App, Response, JSONResponse, TemplateResponse
from wsgiref.simple_server import make_server

app = App()


@app.route('/', 'GET')
def index(request):
    return TemplateResponse('index.html', title="Index", numbers=[1, 2, 3])

@app.route('/hello/(?P<name>\w+)', 'GET')
def hello(request, name): 
    return JSONResponse({'foo':'bar'})

@app.route('/night', 'GET')
def goodnight(request):
    return Response('Hello Night')

if __name__ == '__main__':
    httpd = make_server('', 8000, app)
    httpd.serve_forever()