# coding: utf-8
from __future__ import print_function, unicode_literals

from .handler import LogfireHandler
from .helpers import LogfireContext, DEFAULT_CONTEXT
from .formatter import LogfireFormatter

__version__ = '0.0.1'

context = DEFAULT_CONTEXT