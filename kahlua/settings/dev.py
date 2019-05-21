"""
Development settings

Change this to match your environment
"""

# pylint: disable=wildcard-import,unused-wildcard-import
from .base import *  # noqa: F403,F401

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# SECURITY WARNING: define the correct hosts in production!
ALLOWED_HOSTS = ['*']

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

INSTALLED_APPS = INSTALLED_APPS + [  # noqa: F405
    'debug_toolbar'
]

MIDDLEWARE = MIDDLEWARE + [  # noqa: F405
    'debug_toolbar.middleware.DebugToolbarMiddleware',
]

try:
    # pylint: disable=wildcard-import,unused-wildcard-import
    from .local import *  # noqa: F403,F401
except ImportError:
    pass
