from __future__ import absolute_import, unicode_literals
from .celery import app
import os
import traceback

os.environ['DJANGO_SETTINGS_MODULE'] = 'djauth.settings'
timeformat = "%Y-%m-%d %H:%M:%S"

@app.task
def add(x, y):
    return x + y
