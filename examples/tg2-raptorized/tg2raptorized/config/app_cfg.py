# -*- coding: utf-8 -*-
"""
Global configuration file for TG2-specific settings in tg2-raptorized.

This file complements development/deployment.ini.

Please note that **all the argument values are strings**. If you want to
convert them into boolean, for example, you should use the
:func:`paste.deploy.converters.asbool` function, as in::
    
    from paste.deploy.converters import asbool
    setting = asbool(global_conf.get('the_setting'))
 
"""

from tg.configuration import AppConfig

import tg2raptorized
from tg2raptorized import model
from tg2raptorized.lib import app_globals, helpers 

base_config = AppConfig()
base_config.renderers = []

base_config.package = tg2raptorized

#Enable json in expose
base_config.renderers.append('json')
#Set the default renderer
base_config.default_renderer = 'mako'
base_config.renderers.append('mako')
base_config.use_sqlalchemy=False
base_config.use_ming=False
base_config.use_transaction_manager=False
base_config.auth_backend=None
base_config.use_toscawidgets=False
