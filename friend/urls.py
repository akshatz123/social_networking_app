from django.conf.urls import url
from django.urls import path, include, re_path
from .views import *

urlpatterns = [
    url(r'^add_friend_link/(?P<from_user>[0-9A-Za-z_\-]+)/(?P<to_user>[0-9A-Za-z_\-]+)/$', add_friend_link, name='add_friend_link'),
    re_path(r'^accept_friend_request(?P<from_user>[0-9A-Za-z_\-]+)/(?P<to_user>[0-9A-Za-z_\-]+)/(?P<status>[\w-]+)/$', accept_friend_request, name = 'accept_friend_request')
]