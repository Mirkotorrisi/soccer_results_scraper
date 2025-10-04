from scraper import create_app
from gevent.pywsgi import WSGIServer
from gevent import monkey

app = create_app()

if __name__ == '__main__':
    http_server = WSGIServer(('0.0.0.0', 8085), app)
    http_server.serve_forever()




