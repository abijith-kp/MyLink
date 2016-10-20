#!/usr/bin/python

from links.links import mylink
from wsgiref.simple_server import make_server
from werkzeug.debug import DebuggedApplication

if __name__ == '__main__':
    application = DebuggedApplication(mylink, True)
    httpd = make_server('', 8051, application)
    httpd.serve_forever()
