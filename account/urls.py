from . import views
from django.conf.urls import url

app_name = 'account'
urlpatterns = [
    url(r'^admin_index/$', views.index, name='admin_index'),
    url(r'^admin_login/$', views.LoginView.as_view(), name='admin_login'),
    url(r'^admin_logout/$', views.logout_user, name='admin_logout'),
    url(r'^admin_register/$', views.RegisterUser.as_view(), name='admin_register'),
    url(r'^admin_delete/$', views.UserDelete.as_view(), name='admin_delete'),
    url(r'^admin_add_new_user/$', views.AddNewUser.as_view(), name='admin_add_new_user'),
    url(r'^users_update/(?P<user_pk>.*)/$', views.UserUpdate.as_view(), name='users_update'),
    url(r'^admin_users_list/$', views.UserListView.as_view(), name='admin_users_list'),
]