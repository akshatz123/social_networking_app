import random

from django.http import HttpResponseRedirect

from django_project.settings import AUTH_USER_MODEL
from .models import Posts
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth import get_user_model
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)
from django_project.settings import MEDIA_URL

user = get_user_model()

def home_view(request):
    """Display all the post of friends and own posts on the dashboard"""
    if request.user.is_authenticated:
        context = {
            'posts': Posts.objects.filter(author=request.user).order_by('-date_posted'),
            'media': MEDIA_URL
        }
        return render(request, 'blog/home.html', context)


class PostDetailView(DetailView):
    if user.is_authenticated:
        model = Posts
    else:
        redirect('blog/')

    def get_queryset(self):
        return Posts.objects.filter(author=self.request.user).order_by('date_posted')


class PostCreateView(LoginRequiredMixin, CreateView):

    """Post form has fields
        title
        content
        image
        video
    """
    fields = ['title', 'content', 'image', 'video']
    model = Posts
    success_url = '/blog'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """Post update form  has fields
        title
        content
        image
        video
    """
    model = Posts
    fields = ['title', 'content', 'image', 'video']
    success_url = '/blog'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Posts
    success_url = '/blog'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


def about(request):
    return render(request, 'blog/about.html', {'title': 'About'})


class UserPostListView(ListView):
    model = Posts
    template_name = 'blog/user_posts.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'posts'
    paginate_by = 5
    ordering = ['-date_posted']

    def get_queryset(self):
        user = get_object_or_404(AUTH_USER_MODEL, username=self.kwargs.get('pk'))
        return Posts.objects.filter(author=user).order_by('-date_posted')


def like_post(request):
    posts = get_object_or_404(Posts, id=request.Post.get('post_id'))
    post.likes.add(request.user)
    is_liked = True
    return HttpResponseRedirect(post.get_absolute_url())


class PostDetailView(DetailView):
    model = Posts
    context_object_name = 'post'
    template_name = 'blog/posts_detail.html'
    is_liked = False

    # def get_context_data(self, request, **kwargs):
    #     context = super(PostDetailView, self).get_context_data(request, **kwargs)
    #     posts = context['posts']
    #     if posts.likes.filter(id = request.user.id).exists():
    #         context['is_liked'] = True
    #     return context


def post_draft_list(request):
    posts = Posts.objects.all().order_by('created_date')
    return render(request, 'blog/post_draft_list.html', {'posts': posts})