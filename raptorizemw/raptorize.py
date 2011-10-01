
import BeautifulSoup
import mimetypes
import os
import webob
import wsgiref.util


class ResourcesApp(object):
    def __init__(self, bufsize=1024, res_max_age=86400):
        self.bufsize = bufsize
        self.res_max_age = res_max_age
        self.here = os.sep.join(__file__.split(os.sep)[:-1])
        resource_files = os.listdir(os.sep.join([self.here, 'resources']))
        self.prefix = '/raptorizemw/resources'
        self.served_files = [
            '/'.join([self.prefix, f]) for f in resource_files
        ]

    def will_serve(self, path):
        return path in self.served_files

    def __call__(self, environ, start_response):
        req = webob.Request(environ)

        if not self.will_serve(environ['PATH_INFO']):
            resp = webob.Response(status="404 Not Found")
            return resp(environ, start_response)

        filename = os.sep.join(
            [self.here] + environ['PATH_INFO'].split('/')[2:]
        )

        ct, enc = mimetypes.guess_type(os.path.basename(filename))

        try:
            stream = open(filename)
        except IOError as e:
            resp = webob.Response(status="404 Not Found")
        else:
            stream = wsgiref.util.FileWrapper(stream)
            resp = webob.Response(request=req, app_iter=stream, content_type=ct)
            if enc:
                resp.content_type_params['charset'] = enc
        resp.cache_control = {'max-age': int(self.res_max_age)}
        return resp(environ, start_response)

class RaptorizeMiddleware(object):
    def __init__(self, app, serve_resources=True, **kw):
        self.app = app
        self.serve_resources = serve_resources
        self.resources_app = ResourcesApp()

    def __call__(self, environ, start_response):
        __app__ = None
        if self.serve_resources and 'raptorizemw' in environ['PATH_INFO']:
            __app__ = self.resources_app
        else:
            __app__ = self.app

        req = webob.Request(environ)
        resp = req.get_response(__app__, catch_exc_info=True)

        if self.should_raptorize(req, resp):
            resp = self.raptorize(resp)

        return resp(environ, start_response)

    def should_raptorize(self, req, resp):

        if resp.status != "200 OK":
            return False

        content_type = resp.headers.get('Content-Type', 'text/plain').lower()
        if not 'html' in content_type:
            return False

        # TODO -- Add other criteria here.  Path-based, configurable excepts?

        return True

    def raptorize(self, resp):
        soup = BeautifulSoup.BeautifulSoup(resp.body)

        if not soup.html:
            return resp

        if not soup.html.head:
            soup.html.insert(0, BeautifulSoup.Tag(soup, "head"))

        prefix = self.resources_app.prefix
        js_helper = BeautifulSoup.Tag(
            soup, "script", attrs=[
                ('type', 'text/javascript'),
                ('src', prefix + '/js_helper.js'),
            ])
        soup.html.head.insert(len(soup.html.head), js_helper)

        # TODO -- figure out how to *not* include jquery if its already there
        cdn_base = 'http://ajax.googleapis.com/ajax/libs'
        jquery_url = cdn_base + '/jquery/1.4.3/jquery.min.js'
        jquery_dynamic_include = BeautifulSoup.Tag(
            soup, "script", attrs=[
                ('type', 'text/javascript'),
                ('src', jquery_url),
            ])
        soup.html.head.insert(len(soup.html.head), jquery_dynamic_include)

        raptorize_js = BeautifulSoup.Tag(
            soup, "script", attrs=[
                ('type', 'text/javascript'),
                ('src', prefix + '/jquery.raptorize.1.0.js'),
            ])
        soup.html.head.insert(len(soup.html.head), raptorize_js)

        payload_js = BeautifulSoup.Tag(
            soup, "script", attrs=[
                ('type', 'text/javascript'),
            ])
        payload_js.setString(
            """
            $(window).load(function() {
                $('body').raptorize({
                    enterOn: "timer",
                    delayTime: 2000,
                });
            });
            """
        )
        soup.html.head.insert(len(soup.html.head), payload_js)

        resp.body = str(soup.prettify())
        return resp


def make_middleware(app=None, **kw):
    app = RaptorizeMiddleware(app, **kw)
    return app
