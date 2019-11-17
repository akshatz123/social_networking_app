from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth import get_user_model
from .models import Friend
User = get_user_model()


@login_required(login_url='/login')
def add_friend_link(request, uidb64):
    """Adding a link  in email which is sent to friend through which one can accept or reject friend request"""
    try:
        uid = force_bytes(urlsafe_base64_decode(uidb64))
        # print(uid)
        user = User.objects.get(pk=uid)
        # print(user, "IN TRY BLOCK")
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    return render(request, 'users/accept_friend.html', {"uid": uidb64, "user": user})


@login_required(login_url='/login')
def accept_friend_request(request, uidb64, status):
    """Accept button will lead to entry in database as accepted and reject button will lead to entry in database as rejected  based on status flag"""
    Friend.status = "pending"
    # print(type(Friend))
    try:
        # print('IN try ')
        uid = urlsafe_base64_decode(uidb64)
        # print(uid)
        friend_user = User.objects.filter(id=Friend.to_user.id)
        # print(friend_user)
        # print(User.objects.get(id=Friend.to_user.id))
        f = Friend.objects.filter(friend_id = friend_user)
        if f:
            f.status=status
            f.save()
            f.status = "accepted"
            return render(request, 'users/friend_list.html', {"uidb64": uid, "status": status})
        else:
            f.status = "rejected"
            f.save()
            return render(request, 'users/friend_list.html', {'uidb64':uid, 'status':status})
    except AttributeError:
        return render(request, 'blog/base.html')


def friend_list(request):
    context = {
        'f': User.objects.filter(user_id=Friend.from_user.id)
    }
    return render(request ,'users/friend_list.html', context)