from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.exceptions import FieldError
from django.shortcuts import render, get_object_or_404, redirect
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth import get_user_model
from .models import Friend
from django.forms.models import model_to_dict
User = get_user_model()


@login_required(login_url='/login')
def add_friend_link(request, uidb64):
    """Adding a link  in email which is sent to friend through which one can accept or reject friend request"""
    try:
        uid = force_bytes(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    return  render(request, 'users/accept_friend.html', {"uid": uidb64, "user": user})


@login_required(login_url='/login')
def accept_friend_request(request, uidb64, status):

    """Accept button will lead to entry in database as accepted
    and reject button will lead to entry in database as rejected
    based on status flag"""

    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        friends = Friend.objects.all()
        for f in friends:
            if f:
                f.status = "accepted"
                f.save()
                return render(request, 'users/friend_list.html', {"uidb64": uid, "status":status})
            else:
                f.status = "rejected"
                f.save()
                return render(request, 'users/friend_list.html', {'uidb64':uid, 'status':status})
    except(FieldError, AttributeError):
        return render(request, 'blog/base.html')


def friend_list(request):
    context = {
        'results': Friend.objects.filter(from_user=request.user)
    }
    return render(request ,'users/friend_list.html', context)