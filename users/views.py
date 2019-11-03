from django.db.models import Q
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm
from django.contrib.auth import get_user_model
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from users.models import Profile, FriendRequest
User = get_user_model()


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


def users_list(request):
    users = Profile.objects.exclude(user=request.user)
    context = {
        'users': users
    }
    return render(request, "home.html", context)


def send_friend_request(request, id):
    if request.user.is_authenticated:
        user = get_object_or_404(User, id=id)
        frequest, created = FriendRequest.objects.get_or_create(
            from_user=request.user,
            to_user=user)
        return HttpResponseRedirect('/users')


def cancel_friend_request(request, id):
    if request.user.is_authenticated:
        user = get_object_or_404(User, id=id)
        frequest = FriendRequest.objects.filter(
            from_user=request.user,
            to_user=user).first()
        frequest.delete()
        return HttpResponseRedirect('/users')


def accept_friend_request(request, id):
    from_user = get_object_or_404(User, id=id)
    frequest = FriendRequest.objects.filter(from_user=from_user, to_user=request.user).first()
    print(frequest)
    user1 = frequest.to_user
    user2 = from_user
    user1.profile.friends.add(user2.profile)
    user2.profile.friends.add(user1.profile)
    frequest.delete()
    return HttpResponseRedirect('/users/{}'.format(request.user.profile.slug))


def delete_friend_request(request, id):
    from_user = get_object_or_404(User, id=id)
    frequest = FriendRequest.objects.filter(from_user=from_user, to_user=request.user).first()
    frequest.delete()
    return HttpResponseRedirect('/users/{}'.format(request.user.profile.slug))


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
        return render(request, 'users/profile.html', dict(u_form=u_form, p_form=p_form))


def search(request):
    if request.method == 'GET':
        query = request.GET.get('q')
        if query:
            lookups = Q(first_name=query)
            results = User.objects.filter(Q(first_name=query))
            context = {'results': results}
            # print(context)
            return render(request, 'search.html', context)
        else:
            context = {
                'results': "Not found",
                      }
            return redirect(request, 'search.html', context)
    else:
        return render(request, 'base.html')
