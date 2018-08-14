from . import views
from django.conf.urls import url

app_name = 'core'
urlpatterns = [
    url(r'^feed/$', views.Feed.as_view(), name='feed'),

]