from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.shortcuts import render, get_object_or_404

# Create your views here.
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth import get_user_model
from django_project import settings
from django_project.settings import AUTH_USER_MODEL
from friend.models import Friend
User = get_user_model()
print(User)

@login_required(login_url='/login')
def add_friend_link(request, uidb64):
    """Adding a link  in email which is sent to friend through which one can accept or reject friend request"""
    try:
        uid = force_bytes(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
        print(user)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    return render(request, 'users/accept_friend.html',{"user":user, 'uidb64':uid})


def accept_friend_request(request, uidb64, status):
    uid= force_bytes(urlsafe_base64_decode(uidb64))
    friend_user = User.objects.get(pk=Friend.to_user.id)
    f = Friend.objects.filter(friend_id = friend_user)
    if f:
        f.status=status
        f.save()
        return request,"users/friend_list.html"
    else:
        return render(request, 'blog/base.html')

# def friend_list(request):
#     context = {
#         'f': User.objects.filter(user_id=friend_id)
#     }
#     return render(request ,'users/friend_list.html', context)