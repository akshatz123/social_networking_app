from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.exceptions import FieldError
from django.shortcuts import render, get_object_or_404, redirect
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth import get_user_model
from .models import Friend
User = get_user_model()


@login_required(login_url='/login')
def add_friend_link(request, uidb64, to_user, from_user):
    """Adding a link  in email which is sent to friend through which one can accept or reject friend request"""
    try:
        from_user = force_bytes(urlsafe_base64_decode(uidb64))
        print(from_user)
        uid = force_bytes(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
        to_user = force_bytes(urlsafe_base64_decode(uidb64))
        print(to_user)
        # to_user = User.objects.get(user_id= id)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    return  render(request, 'users/accept_friend.html', {"uid": from_user, "user": user, 'to_user':to_user})


def accept_friend_request(request, from_uid,  to_uid):
    """Accept button will lead to entry in database as accepted
    and reject button will lead to entry in database as rejected
    based on status flag"""
    try:
        from_uid = urlsafe_base64_decode(from_uid).decode()
        to_uid = urlsafe_base64_decode(to_uid).decode()

        friends = Friend.objects.filter(from_uid, to_uid)
        for friend in friends:
            if friend:
                friend.status = "accepted"
                friend.save()
                print(friend.status)
                return render(request, 'users/friend_list.html', {from_uid, to_uid,"accepted"})
            else:
                friend.status = "rejected"
                friend.save()

                return render(request, 'users/friend_list.html', {from_uid, to_uid,'rejected'})
    except(FieldError, AttributeError):
        return render(request, 'blog/base.html')


@login_required(login_url='login/')
def friend_list(request):
    context = {
        'results_from_user': Friend.objects.filter(from_user=request.user)
        # 'result_to_user' :Friend
    }
    return render(request,'users/friend_list.html', context)