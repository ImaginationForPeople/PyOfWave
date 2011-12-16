"""
This package includes any APIs which function to save data to
perminant storage.
"""

from pyofwave.conf import settings
from .utils import load_backend

datastore = None

def initialize():
    datastore = load_backend(settings.DATASOURCE_STORAGE)

