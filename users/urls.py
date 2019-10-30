from django.urls import path
from .views import *

urlpatterns=[
    path('user/<int:user_id>', UserPostListView.as_view(), name='user-post'),
]
