from django.contrib.auth import forms
from django.db import models
from django.contrib.auth.models import User
from PIL import Image
from django_project.settings import AUTH_USER_MODEL


class Profile(models.Model):
    """docstring for Profile"""
    user = models.OneToOneField(AUTH_USER_MODEL, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to="profile_pics")

    def __str__(self):
        msg = '{} Profile'.format(self.user.username)
        return msg

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        img = Image.open(self.image.path)

        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)


class Friend(models.Model):
    users = models.OneToOneField(AUTH_USER_MODEL, on_delete=models.CASCADE)
    current_user = models.ForeignKey(AUTH_USER_MODEL, related_name='owner', null=True, on_delete=models.CASCADE)

    @classmethod
    def make_friend(cls, current_user, new_friend):
        friend, created = cls.objects.get_or_create(
            current_user=current_user
        )
        friend.users.add(new_friend)

    @classmethod
    def lose_friend(cls, current_user, new_friend):
        friend, created = cls.objects.get_or_create(
            current_user=current_user
        )
        friend.users.remove(new_friend)

