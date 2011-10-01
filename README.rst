`Raptorize` WSGI Middleware
===========================

Because every WSGI app is better with a raptor.
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. image:: https://github.com/ralphbean/raptorizemw/raw/master/raptorizemw/resources/raptor.png

Insallation
-----------

You could install it yourself with `pip`::

    $ pip install raptorizemw

Or you could add ``raptorizemw`` to the list of required packages in the
``setup.py`` file of your project.

Usage in TurboGears 2
---------------------

Simply edit ``myapp/config/middleware.py`` and add the following to
``make_app(...)``::

    # Wrap your base TurboGears 2 application with custom middleware here
    import raptorizemw
    app = raptorizemw.make_middleware(app)

Restart your app, but watch out for raptors!

Usage in Pyramid
----------------

Edit ``myapp/__init__.py`` and replace the ``return config.make_wsgi_app()``
line with the following::

    import raptorizemw
    app = config.make_wsgi_app()
    app = raptorizemw.make_middleware(app)
    return app

Credits
-------

This WSGI-fication of the raptorize jquery plugin was written
by `Ralph Bean <http://threebean.org>`_.  Real credit goes to the people over at
ZURB who authored the `original jquery plugin
<http://www.zurb.com/playground/jquery-raptorize>`_.

Get the source
--------------

The code and bug tracker live over at http://github.com/ralphbean/raptorizemw.
Please fork and improve!  We need configurable options.  :)
