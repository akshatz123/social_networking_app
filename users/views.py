from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.views.generic import ListView

from blog.models import Posts
from django_project.settings import AUTH_USER_MODEL
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm
from django.contrib.auth.decorators import login_required
from .models import Profile


def register(request):
	if request.method == 'POST':
		form = UserRegisterForm(request.POST)
		if form.is_valid():
			form.save()
			form.cleaned_data.get('username')
			msg = 'Your account is created ! You are now able to login'
			messages.success(request, msg)
			return redirect('login')
	else:
		form = UserRegisterForm() 
	return render(request, 'users/register.html', {'form': form})


@login_required
def profile(request):
	if request.method == 'POST':
		u_form = UserUpdateForm(request.POST, instance=request.user)
		p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
		if u_form.is_valid() and p_form.is_valid():
			u_form.save()
			p_form.save()
			msg = 'Your account has been successfully updated!'
			messages.success(request, msg)
			return redirect('profile')
	else:
		u_form = UserUpdateForm(instance=request.user)
		p_form = ProfileUpdateForm(instance=request.user)
	context = {
		'u_form': u_form,
		'p_form': p_form
	}
	return render(request, 'users/profile.html', context)


class UserPostListView(ListView):
	model = Posts
	print(model)
	template_name = 'blog/user_posts.html'  # <app>/<model>_<viewtype>.html
	print(template_name)
	context_object_name = 'posts'
	print(context_object_name)
	paginate_by = 5

	def get_queryset(self):
		user = get_object_or_404(AUTH_USER_MODEL, username=self.kwargs.get('username'))
		print(user)
		return Posts.objects.filter(author=AUTH_USER_MODEL).order_by('-date_posted')


