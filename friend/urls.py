from django.conf.urls import url
from django.urls import path, include
from .views import *

urlpatterns = [
    url(r'^add_friend_link/(?P<uidb64>[0-9A-Za-z_\-]+)/$', add_friend_link, name='add_friend_link'),
    url(r'^accept_friend_request/(?P<uidb64>[0-9A-Za-z_\-]+)/$', accept_friend_request, name='accept_friend_request')

]