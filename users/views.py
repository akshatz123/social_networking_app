from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.db.models import Q
from django.shortcuts import render, redirect
from django.contrib import messages
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.views import View

from .token_generator import account_activation_token
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm
from django.contrib.auth import get_user_model, login
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, get_object_or_404
from users.models import Profile, FriendRequest
User = get_user_model()


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            email_subject = 'Activate Your Account'
            message = render_to_string('activate_account.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(email_subject, message, to=[to_email])
            email.send()
            return HttpResponse('We have sent you an email, please confirm your email address to complete registration')
    else:
        form = UserRegisterForm()
    return render(request, 'users/login.html', {'form': form})


def activate_account(request, uidb64, token):
    try:
        uid = force_bytes(urlsafe_base64_decode(uidb64))
        print(uid)
        user = User.objects.get(pk=uid)
        print(user)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        return HttpResponse('Your account has been activate successfully')
    else:
        return HttpResponse('Activation link is invalid!')


def users_list(request):
    users = Profile.objects.exclude(user=request.user)
    context = {
        'users': users
    }
    return render(request, "home.html", context)


def send_friend_request(request, id):
    if request.user.is_authenticated:
        user = get_object_or_404(User, id=id)
        frequest, created = FriendRequest.objects.get_or_create(from_user=request.user,to_user=user)
        return HttpResponseRedirect('home_view')


def cancel_friend_request(request, id):
    if request.user.is_authenticated:
        user = get_object_or_404(User, id=id)
        frequest = FriendRequest.objects.filter(
            from_user=request.user,
            to_user=user).first()
        frequest.delete()
        return HttpResponseRedirect('home_view')


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
