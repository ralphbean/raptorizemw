
import BeautifulSoup
import datetime
import random
import webob

import raptorizemw.resources


class RaptorizeMiddleware(object):
    """ WSGI middleware that throws a raptor on your page. """

    def __init__(self, app, serve_resources=True, random_chance=1.0,
                 only_on_april_1st=False, enterOn='timer', delayTime=2000,
                 **kw):
        """ Configuration arguments are documented in README.rst

        Also at http://pypi.python.org/pypi/raptorizemw
        """

        if not enterOn in ['timer', 'konami-code']:
            raise ValueError("enterOn must be either 'timer' or 'konami-code'")

        self.resources_app = raptorizemw.resources.ResourcesApp()

        self.app = app
        self.serve_resources = serve_resources
        self.random_chance = float(random_chance)
        self.only_on_april_1st = bool(only_on_april_1st)
        self.enterOn = enterOn
        self.delayTime = int(delayTime)

    def __call__(self, environ, start_response):
        """ Process a request.

        Do one of two things::

            - If this request is for a raptor resource (image, sound, js
              code).  Ignore the next WSGI layer in the call chain and just
              serve the resource myself.
            - Call the next layer in the WSGI call chain and retrieve its
              output.  Determine if I should actually raptorize this request
              and if so, insert our magic javascript in the <head> tag.
        """
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
        """ Determine if this request should be raptorized.  Boolean. """

        if resp.status != "200 OK":
            return False

        content_type = resp.headers.get('Content-Type', 'text/plain').lower()
        if not 'html' in content_type:
            return False

        if random.random() > self.random_chance:
            return False

        if self.only_on_april_1st:
            now = datetime.datetime.now()
            if now.month != 20 and now.day != 1:
                return False

        return True

    def raptorize(self, resp):
        """ Raptorize this response!

        Insert javascript into the <head> tag.

        If jquery is already included, make sure not to stomp on it by
        re-including it.
        """

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

        payload_js = BeautifulSoup.Tag(
            soup, "script", attrs=[
                ('type', 'text/javascript'),
            ])
        payload_js.setString(
            """
            run_with_jquery(function() {
                include_js("%s", function() {
                    $(window).load(function() {
                        $('body').raptorize({
                            enterOn: "%s",
                            delayTime: %i,
                        });
                    });
                })
            });
            """ % (
                prefix + '/jquery.raptorize.1.0.js',
                self.enterOn,
                self.delayTime
            )
        )
        soup.html.head.insert(len(soup.html.head), payload_js)

        resp.body = str(soup.prettify())
        return resp


def make_middleware(app=None, *args, **kw):
    """ Given an app, return that app wrapped in RaptorizeMiddleware """
    app = RaptorizeMiddleware(app, *args, **kw)
    return app
