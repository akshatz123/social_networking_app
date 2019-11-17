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
        uid = urlsafe_base64_decode(uidb64).decode()
        # print(uid)
        user = User.objects.get(pk=uid)
        # print(user, "IN TRY BLOCK")
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    return render(request, 'users/accept_friend.html', {"uid": uidb64, "user": user})


@login_required(login_url='/login')
def accept_friend_request(request, uidb64, status):
    """Accept button will lead to entry in database as accepted and reject button will lead to entry in database as rejected  based on status flag"""
    uid= urlsafe_base64_decode(uidb64).decode()
    try:
        friend_user = User.objects.get(id=Friend.to_user.friend_id)
        print(friend_user)
        f = Friend.objects.filter(friend_id = friend_user)
        if f:
            f.status=status
            f.save()
            return request, "users/friend_list.html", {"uid": uidb64,"status": status}
    except(ValueError, AttributeError):
        return (request, 'blog/base.html')

# def friend_list(request):
#     context = {
#         'f': User.objects.filter(user_id=friend_id)
#     }
#     return render(request ,'users/friend_list.html', context)