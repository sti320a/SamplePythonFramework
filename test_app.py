from app import App, Response
from wsgiref.simple_server import make_server

app = App()

@app.route('/(?P<name>\w+)', 'GET')
def hello(request, name): 
    return Response('Hello {name}'.format(name=name), headers={'foo':'bar'})

@app.route('/night', 'GET')
def goodnight(request):
    return Response('Hello World')

if __name__ == '__main__':
    httpd = make_server('', 8000, app)
    httpd.serve_forever()