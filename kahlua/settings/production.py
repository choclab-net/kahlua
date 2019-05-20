"""
Production settings
"""
# pylint: disable=wildcard-import,unused-wildcard-import
from .base import *  # noqa: F403,F401

DEBUG = False
ALLOWED_HOSTS = ['choclab.net', 'www.choclab.net', 'kahlua.choclab.net']
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

try:
    from .local import *  # noqa #F403, F401
except ImportError:
    pass
