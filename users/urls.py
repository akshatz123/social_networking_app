import django.conf.urls
from django.conf.urls.i18n import urlpatterns
from django.urls import path
from .views import *

urlpatterns = [
    django.conf.urls.url('friend-request/send/(?P<id>[\w-]+)/$', send_friend_request, name='send_friend_request'),
    django.conf.urls.url('friend-request/cancel/(?P<id>[\w-]+)/$', cancel_friend_request, name='cancel_friend_request'),
    django.conf.urls.url('friend-request/accept/(?P<id>[\w-]+)/$', accept_friend_request, name='accept_friend_request'),
    path('search/', search, name='friends_search'),
]
