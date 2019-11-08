from django.db import models
from django.contrib.auth.models import AbstractUser
from django.urls import reverse
from PIL import Image
from django_project.settings import AUTH_USER_MODEL
# from friendship.models import Friend, Follow, Block
import uuid


class User(AbstractUser):
    """
        Custom User model will be having user id as primary key, first_name, last_name and username
        will be imported from AbstractUser model
        Date of birth for entering date of birth
    """
    email = models.EmailField(max_length=255, unique=True)
    dateofbirth = models.DateField(null=True)
    # friend_id = models.ManyToManyField('self')
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.username


class Posts(models.Model):
    """
    Post has title, content, image, video and author fields which are visible to user.
    """

    title = models.CharField(max_length=100)
    content = models.TextField()
    date_posted = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE)
    image = models.ImageField(upload_to="profile_pics", default='default.jpg', null=True)
    date_modified = models.DateTimeField(auto_now=True, blank=True)
    video = models.FileField(upload_to='', null=True, verbose_name="video")
    likes = models.ManyToManyField(User, related_name='likes', blank=True)
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'pk': self.pk})

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        img = Image.open(self.image.path)

        if img.height > 300 or img.wid0th > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)

    @property
    def photo_url(self):
        if self.image and hasattr(self.image, 'url'):
            return self.image.url


class Comment(models.Model):
    post = models.ForeignKey('Posts', on_delete=models.CASCADE, related_name='comments')
    author = models.CharField(max_length=200)
    text = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)
    approved_comment = models.BooleanField(default=False)

    def approve(self):
        self.approved_comment = True
        self.save()

    def __str__(self):
        return self.text