# -*- coding: utf-8 -*-
"""Main Controller"""

from tg import expose, flash, require, url, request, redirect
from tg.i18n import ugettext as _, lazy_ugettext as l_

from tg2raptorized.lib.base import BaseController
from tg2raptorized.controllers.error import ErrorController

__all__ = ['RootController']


class RootController(BaseController):
    """
    The root controller for the tg2-raptorized application.

    All the other controllers and WSGI applications should be mounted on this
    controller. For example::

        panel = ControlPanelController()
        another_app = AnotherWSGIApplication()

    Keep in mind that WSGI applications shouldn't be mounted directly: They
    must be wrapped around with :class:`tg.controllers.WSGIAppController`.

    """

    error = ErrorController()

    @expose('tg2raptorized.templates.index')
    def index(self):
        """Handle the front-page."""
        return dict(page='index')

    @expose('tg2raptorized.templates.about')
    def about(self):
        """Handle the 'about' page."""
        return dict(page='about')

    @expose('tg2raptorized.templates.environ')
    def environ(self):
        """This method showcases TG's access to the wsgi environment."""
        return dict(environment=request.environ)

    @expose('tg2raptorized.templates.data')
    @expose('json')
    def data(self, **kw):
        """This method showcases how you can use the same controller for a data page and a display page"""
        return dict(params=kw)
