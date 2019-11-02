from django.conf.urls import url

from .views import (
    send_friend_request,
    cancel_friend_request,
    accept_friend_request,
    delete_friend_request
)

urlpatterns = [
    url('friend-request/send/(?P<id>[\w-]+)/$', send_friend_request, name='send_friend_request'),
    url('friend-request/cancel/(?P<id>[\w-]+)/$', cancel_friend_request, name='cancel_friend_request'),
    url('friend-request/accept/(?P<id>[\w-]+)/$', accept_friend_request, name='accept_friend_request'),
    url('friend-request/delete/(?P<id>[\w-]+)/$', delete_friend_request, name='delete_friend_request'),
]
