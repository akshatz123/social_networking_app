from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.urls import reverse
from PIL import Image

from django_project import settings
from django_project.settings import AUTH_USER_MODEL
import uuid


class Friend:

    """
    Model Friend:
    FriendID as primary key
    user_id as foreign key
    status flag for accepting, rejecting the friend requests and null =True, when user is created
    Date created will be automatically added as friend request is send by other user
    Date modified will be automatically be added when friend request is accepted or cancelled
    """
    friend_id = models.IntegerField(primary_key=True)
    user_id = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE)
    status_flag = models.CharField()
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)


class User(AbstractUser):
    """
    Custom User model will be having user id as primary key, first_name, last_name and username
    will be imported from AbstractUser model
    Date of birth for entering date of birth
    """
    email = models.EmailField(max_length=255, unique=True)
    dateofbirth = models.DateField(null=True)
    friend_id = models.ManyToManyField('self', Friend)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.username


class Posts(models.Model):
    """
    Post has title, content, image and author fields which are visible to user.
    """
    title = models.CharField(max_length=100)
    content = models.TextField()
    date_posted = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE)
    image = models.ImageField(upload_to="profile_pics", blank=True, null=True, default='')
    date_modified = models.DateTimeField(auto_now=True, blank=True)
    video = models.FileField(upload_to='', null=True, verbose_name="Video")
    likes = models.ManyToManyField(User, related_name='likes', blank=True)
    uuid = models.UUIDField(default=uuid.uuid4, primary_key=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'pk': self.pk})

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        img = Image.open(self.image.path)

        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)

    @property
    def photo_url(self):
        if self.image and hasattr(self.image, 'url'):
            return self.image.url


class Like(models.Model):
    user = models.ForeignKey(getattr(settings, 'AUTH_USER_MODEL', 'auth.User'), on_delete=models.CASCADE)
    target_content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    target_object_id = models.PositiveIntegerField()
    target = GenericForeignKey('target_content_type', 'target_object_id')
    timestamp = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        ordering = ["-timestamp"]
        get_latest_by = "timestamp"
        unique_together = ("user", "target_content_type", "target_object_id")
        verbose_name = "like"
        verbose_name_plural ="likes"

    def __str__(self):
        return u"{} liked {}".format(self.user, self.target)

class Comment(models.Model):
    user = models.ForeignKey(AUTH_USER_MODEL, default=1)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
