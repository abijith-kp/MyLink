#!/usr/bin/python

from links.links import links_app
from wsgiref.simple_server import make_server
from werkzeug.debug import DebuggedApplication

if __name__ == '__main__':
    application = DebuggedApplication(links_app, True)
    httpd = make_server('192.168.0.106', 8051, application)
    httpd.serve_forever()
