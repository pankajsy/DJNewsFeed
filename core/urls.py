from . import views
from django.conf.urls import url

app_name = 'core'
urlpatterns = [
    url(r'^feed/$', views.ArticleFeed.as_view(), name='feed'),

]