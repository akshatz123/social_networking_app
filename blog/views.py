from django.http import request, HttpResponseRedirect
from friendship.models import Friend, Follow, Block
from django.shortcuts import render, get_object_or_404, render_to_response
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)

from blog.forms import FriendMgmtForm
from users.models import Profile
from .models import Posts, FriendMgmt
from PIL import Image


def home(request):
    context = {
        'posts': Posts.objects.all()
    }
    return render(request, 'blog/home.html', context)


class PostListView(ListView):
    model = Posts
    template_name = 'blog/home.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by = 5


class PostDetailView(DetailView):
    model = Posts


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Posts
    fields = ['title', 'content', 'image']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Posts
    fields = ['title', 'content', 'image']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        img = Image.open(self.image.path)

        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Posts
    success_url = '/'

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

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Posts.objects.filter(author=user).order_by('-date_posted')


# def profile(request, UserCreationForm):
#     if form.is_valid():
#         form1 = form.save(commit=False)
#         form1.creator = request.user
#         form1.save()
#

# from django_project.settings import AUTH_USER_MODEL
# from friendship.models import Friend, Follow, Block
# from friendship.models import FriendshipRequest

#
# def my_view():
#     other_user = User.objects.get(pk=1)
#     Friend.objects.add_friend(
#         request.AUTH_USER_MODEL,  # The sender
#         other_user,  # The recipient
#         message='Hi! I would like to add you')
#
#     def make_friend(cls, current_user, new_friend):
#         try:
#             friend, created = cls.objects.get_or_create(current_user=current_user)
#             friend.users.add(new_friend)
#
#         except SyntaxError:
#             pass

# def my_friends(request):
#     """
#         used for Displaying and managing friends
#     """
#     if request.method == 'POST':
#
#         form = FriendMgmtForm(request.POST)
#         if form.is_valid():
#
#             user = User.objects.get(id=80)
#             friend_manage = FriendMgmt(user=request.user, friend= user)
#             friend_manage.save()
#         return HttpResponseRedirect('myfriends/')
#
#     else:
#         form = PostCreateView()
#
#         user = request.user
#         profile = Profile.objects.get(user=user)
#         full_name = user.get_full_name()
#         email = user.email
#         friends = FriendMgmt.objects.filter(user=request.user)
#         context = {'form': form,
#             'full_name': full_name,
#             'email': email,
#             'friends': friends
#            }
#         return render_to_response('friends.html', context)