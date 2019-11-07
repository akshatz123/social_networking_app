from django.conf.urls import url
from django.urls import path, include

from .views import (
    home_view,
    PostDetailView,
    PostCreateView,
    PostUpdateView,
    PostDeleteView,
    UserPostListView,
)
from .views import *

urlpatterns = [
    path('', home_view, name='blog-home'),
    path('user/<int:pk>', UserPostListView.as_view(), name='user-posts'),
    # path('post/<int:pk>', PostDetailView.as_view(), name='post-detail'),
    path('post/(?P<pk>[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12})/$', PostDetailView.as_view(), name='post-detail'),
    path('post/new/', PostCreateView.as_view(), name='post-create'),
    path('post/P<pk>[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12})/$', PostUpdateView.as_view(), name='post-update'),
    path('post/P<pk>[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12})/$', PostDeleteView.as_view(), name='post-delete'),
    path('about/', about, name='blog-about'),
    url('likes/', like_post, name='likes_post'),
]
