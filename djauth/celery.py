from __future__ import absolute_import, unicode_literals
import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'djauth.settings'
from celery import Celery

app = Celery('djauth',
             broker='amqp://',
             backend='amqp://',
             include=['djauth.tasks'])

# Optional configuration, see the application user guide.
app.conf.update(
    result_expires=3600,
)

if __name__ == '__main__':
    app.start()