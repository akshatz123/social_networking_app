from django.urls import path

from .views import (
    home_view,
    PostDetailView,
    PostCreateView,
    PostUpdateView,
    PostDeleteView,
    UserPostListView,
)
from . import views

urlpatterns = [
    path('', home_view, name='blog-home'),
    path('user/<int:pk>', UserPostListView.as_view(), name='user-posts'),
    path('post/P<pk>[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12})/$', PostDetailView.as_view(),
         name='post-detail'),
    path('post/P<pk>[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12})/update', PostUpdateView.as_view(),
         name='post-update'),
    path('post/new/', PostCreateView.as_view(), name='post-create'),
    path('post/P<pk>[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12})/delete', PostDeleteView.as_view(),
         name='post-delete'),
    # path('post/likes'
    path('about/', views.about, name='blog-about'),
]
