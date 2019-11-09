from django.http import HttpResponseNotAllowed, HttpResponseBadRequest, HttpResponse

from django_project.settings import AUTH_USER_MODEL
from .models import Posts, Like
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
        return Posts.objects.all().order_by('date_posted')


class PostCreateView(LoginRequiredMixin, CreateView):
    """Post form has fields
        title
        content
        image
        video
    """
    fields = ['title', 'content', 'image', 'video']
    model = Posts

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

#
# def like_post(request):
#     liked = False
#     if request.method == 'GET':
#         post_id = request.GET['post_id']
#         post = Posts.objects.get(id=int(post_id))
#         if request.session.get('has_liked_' + post_id, liked):
#             print("unlike")
#             if post.likes > 0:
#                 likes = post.likes - 1
#                 try:
#                     del request.session['has_liked_' + post_id]
#                 except KeyError:
#                     print("keyerror")
#         else:
#             print("like")
#             request.session['has_liked_' + post_id] = True
#             likes = post.likes + 1
#     post.likes = likes
#     print("updated liked ", post.likes)
#     post.save()
#     return HttpResponse(likes, liked)


def like_post(request):
    if not request.is_ajax():
        return HttpResponseNotAllowed()

    user = request.user

    try:
        app_model = request.POST["target_model"]
        obj_id = int(request.POST["target_object_id"])
    except (KeyError, ValueError):
        return HttpResponseBadRequest()

    like = Like.objects.get_like(user, obj_id, model=app_model)

    if like is None:
        Like.objects.create(user, obj_id, app_model)
        status = 'added'
    else:
        like.delete()
        status = 'deleted'

    likeCount = Like.objects.for_object(obj_id, app_model).count()

    return HttpResponse(status + "|" + str(likeCount))

