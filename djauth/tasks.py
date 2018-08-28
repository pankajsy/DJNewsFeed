from __future__ import absolute_import, unicode_literals

from djauth.settings import BASE_NEWS_API, NEWS_API_KEY, SOURCE_API, TOP_STORIES_API
from .celery import app
import os, json, requests, io, boto3
import traceback
from core.models import Source, Article

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

import datetime
default_image = "https://drive.google.com/file/d/1tdCpzV72TWu5CDVfgspzXqK2bQOL1SDX/view?usp=sharing"
def topdata_apicollectdata():
    category = ['business', 'entertainment', 'general', 'health', 'science', 'sports', 'technology']
    country = ['us', 'in']
    for t in category:
        for c in country:
            url = BASE_NEWS_API + TOP_STORIES_API+"?country="+c+"&category="+t+"&apiKey="+NEWS_API_KEY
            try:
                res = requests.get(url).json()
                if res.get('status')=='ok':
                    # print(res)
                    articles = res.get('articles')
                    for s in articles:
                        # print(s)
                        author= s.get('author') if 'author' in s else ''
                        title= s.get('title') if 'title' in s else ''
                        description= s.get('description') if 'description' in s else ''
                        url= s.get('url') if 'url' in s else ''
                        urltoimage= s.get('urlToImage') if 'urlToImage' in s else default_image
                        published_at= s.get('publishedAt') if 'publishedAt' in s else ''

                        published_at = datetime.datetime.strptime(str(published_at), "%Y-%m-%dT%H:%M:%SZ")
                        source_uid = s.get('source').get('id') if 'source' in s else ''
                        source_name = s.get('source').get('name') if 'source' in s else ''
                        # source_obj, created_s = Source.objects.update_or_create(uid=source_uid,
                        #                                                   defaults={
                        #                                                       "name": source_name,
                        #                                                       "uid": source_uid,
                        #                                                   })
                        artil = Article.objects.create(article_source_id = source_uid,
                                                                article_source = source_name,
                                                                  published_at = published_at,
                                                                  author = author,
                                                                  title = title,
                                                                  desc = description,
                                                                  url = url,
                                                                  urltoimage = urltoimage,
                                                                  category = t,
                                                                  country = c
                                                                  )
                        print (artil.title)
            except Exception as e:
                print (e.message)