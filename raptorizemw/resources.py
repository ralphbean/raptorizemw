
import mimetypes
import os
import webob
import wsgiref.util


class ResourcesApp(object):
    """ Modified from the resources app found in ToscaWidgets2.

    Serve resources for RaptorizeMiddleware.
    """
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
        """ Process a request. """

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
