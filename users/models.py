from django.db import models
from PIL import Image
from django.db.models.signals import post_save
from django.utils.text import slugify

from django_project.settings import AUTH_USER_MODEL


class Profile(models.Model):
    """Updating profile of particular user """
    user = models.OneToOneField(AUTH_USER_MODEL, on_delete=models.CASCADE)
    friends = models.ManyToManyField("Profile", blank=True)
    image = models.ImageField(default='default.jpg', upload_to="profile_pics",  null=True)
    date_modified = models.DateTimeField(auto_now=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return str(self.user.username)

    def __str__(self):
        msg = '{} Profile'.format(self.user.username)
        return msg


# def post_save_user_model_receiver(sender, instance, created, *args, **kwargs):
#     if created:
#         try:
#             Profile.objects.create(user=instance)
#         except:
#             pass


# post_save.connect(post_save_user_model_receiver, sender=AUTH_USER_MODEL)


def save(self, *args, **kwargs):
    super().save(*args, **kwargs)

    img = Image.open(self.image.path)

    if img.height > 300 or img.width > 300:
        output_size = (300, 300)
        img.thumbnail(output_size)
        img.save(self.image.path)


class FriendRequest(models.Model):
    to_user = models.ForeignKey(AUTH_USER_MODEL, related_name='to_user', on_delete=models.CASCADE)
    from_user = models.ForeignKey(AUTH_USER_MODEL, related_name='from_user', on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "From {}, to {}".format(self.from_user.username, self.to_user.username)

