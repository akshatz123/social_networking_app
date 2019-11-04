from django.conf.urls import url
from django.conf.urls.i18n import urlpatterns
from django.urls import path
from .views import *
urlpatterns =[
    url('friend-request/send/(?P<id>[\w-]+)/$', send_friend_request, name='send_friend_request'),
    url('friend-request/cancel/(?P<id>[\w-]+)/$', cancel_friend_request, name='cancel_friend_request'),
    url('friend-request/accept/(?P<id>[\w-]+)/$', accept_friend_request, name='accept_friend_request'),
    path('search/', search, name='friends_search'),
    ]