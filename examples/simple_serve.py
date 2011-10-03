#!/usr/bin/env python

from raptorizemw import make_middleware
import weberror.errormiddleware

if __name__ == '__main__':
    def app(environ, start_response):
        start_response('200 OK', [('Content-Type', 'text/html')])
        return ["<html><body>This is a simple app.</body></html>"]

    # Raptorize!
    app = make_middleware(
        app,
        delayTime=500,
        enterOn='konami-code',
    )

    # Debugging information!
    app = weberror.errormiddleware.ErrorMiddleware(app, debug=True)

    from wsgiref.simple_server import make_server
    httpd = make_server('localhost', 8081, app)
    try:
        print "Serving at localhost:8081..."
        httpd.serve_forever()
    except KeyboardInterrupt:
        print '^C'

