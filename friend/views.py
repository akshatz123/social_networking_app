from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site
from django.core.exceptions import FieldError
from django.core.mail import EmailMessage
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.template.loader import render_to_string
from django.urls import reverse_lazy, reverse
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from blog.models import User
from blog.views import user
from friend.models import Friend, Share

User = get_user_model()


@login_required(login_url='login/')
def friend_list(request):
    context = {
        'results_from_user': Friend.objects.filter(from_user=request.user),
        'results_to_user': Friend.to_user
    }
    # print(context)
    return render(request, 'friend/friend_list.html', context)


@login_required(login_url='/login')
def add_friend_link(request, uidb64):
    """Adding a link  in email which is sent to friend
     through which one can accept or reject friend request"""

    try:
        uid = force_bytes(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=request.user.id)
        return render(request, 'friend/accept_friend.html', {"uid": uidb64, "user": user})
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
        return render(request, reverse_lazy('list'))


def accept_friend_request(request, uidb64, status):
    """Accept button will lead to entry in database as accepted
    and reject button will lead to entry in database as rejected
    based on status flag"""
    try:
        to_user = request.user.id
        uid = force_bytes(urlsafe_base64_decode(uidb64)).decode()
        friends = Friend.objects.all()
        for f in friends:
            if f:
                f.status = "accepted"
                f.save()
                return render(request, 'friend/friend_list.html')
            else:
                f.status = "rejected"
                f.save()
                redirect(reverse_lazy('list'))
    except(FieldError, AttributeError):
        return render(request, 'blog/base.html')


@login_required(login_url='login/')
def add_friend(request, pk):
    """Sending friend request to email"""
    name = request.user.first_name
    from_user = get_object_or_404(User, id=request.user.id)
    current_site = get_current_site(request)
    to_user = get_object_or_404(User, pk=pk)

    email_subject = 'Friend Request from ' + name
    message = render_to_string('friend/add_friend.html', {
        'user': user,
        'domain': current_site.domain,
        'uid': urlsafe_base64_encode(force_bytes(user.pk))
    })
    to_email = to_user.email
    f = Friend(from_user=from_user, to_user=to_user, status="pending")
    context = {'name': name, 'first_name': to_user.first_name, 'last_name': to_user.last_name}
    email = EmailMessage(email_subject, message, from_user.email, to=[to_email])
    email.send()
    if (f.from_user and f.to_user) or (f.from_user == f.to_user):
        return HttpResponseRedirect(reverse(friend_list))
    else:
        f.save()
        return render(request, 'friend/sent_friend_request_success.html', context)


def sharing_of_post(request):
    if Friend.status == 'accepted':
        return render(request,'blog/home.html')
