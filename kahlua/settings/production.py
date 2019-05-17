"""
Production settings
"""
# pylint: disable=wildcard-import,unused-wildcard-import
from .base import *  # noqa: F403,F401

DEBUG = False

try:
    # noqa
    from .local import *  # noqa #F403, F401
except ImportError:
    pass
