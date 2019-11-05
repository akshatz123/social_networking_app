from django.conf.urls import url
from django.urls import path
from .views import *

urlpatterns = [
    url(r'^friend-request/send/(?P<id>[\w-]+)/$', send_friend_request, name='send_friend_request'),
    url(r'^friend-request/cancel/(?P<id>[\w-]+)/$', cancel_friend_request, name='cancel_friend_request'),
    url(r'^friend-request/accept/(?P<id>[\w-]+)/$', accept_friend_request, name='accept_friend_request'),
    path('search/', search, name='friends_search'),
    url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        activate_account, name='activate'),
]
