from __future__ import absolute_import, unicode_literals

from djauth.settings import BASE_NEWS_API, NEWS_API_KEY, SOURCE_API
from .celery import app
import os, json, requests, io, boto3
import traceback
from core.models import Source
os.environ['DJANGO_SETTINGS_MODULE'] = 'djauth.settings'
timeformat = "%Y-%m-%d %H:%M:%S"

@app.task
def add(x, y):
    return x + y

# @app.tasks
def apicollectdata():
    url = BASE_NEWS_API + SOURCE_API+"?apiKey="+NEWS_API_KEY
    try:
        res = requests.get(url).json()
        if res.get('status')=='ok':
            sources = res.get('sources')
            for s in sources:
                uid= s.get('id') if 'id' in s else ''
                name= s.get('name') if 'name' in s else ''
                description= s.get('description') if 'description' in s else ''
                url= s.get('url') if 'url' in s else ''
                category= s.get('category') if 'category' in s else ''
                language= s.get('language') if 'language' in s else ''
                country= s.get('country') if 'country' in s else ''

                source, created = Source.objects.update_or_create(uid = uid,
                                                                  defaults={
                                                                      "name":name,
                                                                      "uid":uid,
                                                                      "desc":description,
                                                                      "url":url,
                                                                      "category": category,
                                                                      "language":language,
                                                                      "country":country
                                                                       })
                print (created)
    except Exception as e:
        print (e.message)
