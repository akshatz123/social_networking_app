from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.db.models import Q
from django.contrib import messages
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode


from blog.views import user
from django_project.settings import MEDIA_URL
from .token_generator import account_activation_token
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm
from django.contrib.auth import get_user_model, login
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from users.models import Profile
from django.contrib.auth.decorators import login_required
from blog.models import Posts, Friend

User = get_user_model()


def register(request):
    """Send Email to confirm validate user"""
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            email_subject = 'Activate Your Account'
            message = render_to_string('users/account_activate.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(email_subject, message, to=[to_email])
            email.send()
            return render(request, 'users/email_sent.html')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})


def activate_account(request, uidb64, token):
    """Activate the account for the user using token and uid"""
    try:
        uid = force_bytes(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        return HttpResponse('Your account has been activate successfully')
    else:
        return render(request, 'Activation link is invalid!')


def users_list(request):
    """TO list all friends of a user"""
    users = Profile.objects.exclude(user=request.user)
    context = {
        'users': users
    }
    return render(request, "home.html", context)


def profile(request):
    """Profile to view the profile"""
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            msg = 'Your account has been successfully updated!'
            messages.success(request, msg)
            return render(request, 'users/profile.html', dict(u_form=u_form, p_form=p_form))
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user)
        return render(request, 'users/profile.html', dict(u_form=u_form, p_form=p_form))


def search(request):
    """Search feature used to search friends """
    if request.method == 'GET':
        query = request.GET.get('q')
        if query is not None and request.user:
            results = User.objects.filter(Q(username=query) | Q(first_name=query) | Q(last_name=query))
            return render(request, 'users/search.html', {'results': results, 'media': MEDIA_URL})
        return render(request, 'base.html')


def search_profile(request, pk):
    """User search Profile"""
    if request.user.is_authenticated:
        if request.method == 'POST':
            u_form = UserUpdateForm(request.POST, instance=request.user)
            p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
            msg = 'Your account has been successfully updated!'
            messages.success(request, msg)
            return render(request, 'users/profile.html', dict(u_form=u_form, p_form=p_form))
    else:
        return render(request, 'users/search_profile.html')


def profile_detail(request, pk):
    user = get_object_or_404(User, pk=pk)
    profile = get_object_or_404(Profile, pk=pk)
    context = dict(first_name=user.first_name,
                   last_name=user.last_name,
                   dateofbirth=user.dateofbirth,
                   email=user.email,
                   username=user.username,
                   image=profile.image.url
                   )
    if request.user.id == user.pk:
        return render(request, 'users/view_profile.html', context)
    else:
        return render(request, 'users/search_profile.html', context)


def add_friend(request, pk):
    # import pdb
    """Sending friend request to email"""
    name = request.user.first_name
    # pdb.set_trace()
    from_user = request.user.email
    # print(from_user)
    current_site = get_current_site(request)
    to_user = get_object_or_404(User, pk=pk)
    # print(to_user.email)
    try:
        email_subject = 'Friend Request from ' + name
        message = render_to_string('users/add_friend.html', {
                    'user': user,
                    'domain': current_site.domain,
                    'uid' : urlsafe_base64_encode(force_bytes(user.pk))
                 })
        # message = 'You have  a friend request from' + from_user
        to_email = to_user.email
        email = EmailMessage(email_subject, message, from_user, to=[to_email])
        email.send()
        context = {'name':name,'first_name':to_user.first_name,'last_name':to_user.last_name }
        f = Friend(user_id=request.user.id, friend_id=to_user.id,status='Pending')
        f.save()
        return render(request, 'users/sent_friend_request_success.html', context)
    except:
        # messages.error("No such user")
        redirect ("NO such user")

@login_required(login_url='/login')
def add_friend_link(request, uidb64):
    """Adding a link  in email which is sent to friend through which one can accept or reject friend request"""
    try:
        # import pdb ; pdb.set_trace()
        uid = force_bytes(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    return render(request, 'users/accept_friend.html',{"user":user, 'uidb64':uid, })


def accept_friend_request(request, uidb64, status):
    uid= force_bytes(urlsafe_base64_decode(uidb64))
    friend_user = User.objects.get(pk=uid)
    f = Friend.objects.filter(friend_id = friend_user)
    if f:
        f.status=status
        f.save()
    return render(request, 'base.html')

@login_required(login_url='/login')
def home(request):
    """Display all the post of friends and own posts on the dashboard"""
    context = {
        'posts': Posts.objects.filter(author=request.user).order_by('-date_posted'),
        'media': MEDIA_URL
    }
    return render(request, 'blog/home.html', context)
