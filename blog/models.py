from django.db import models
from django.contrib.auth.models import AbstractUser
from django.urls import reverse
from PIL import Image
from django.core.files.storage import FileSystemStorage
from django_project.settings import AUTH_USER_MODEL
# fs = FileSystemStorage(location='posts/')


class Friend:
    friend_id = models.IntegerField(primary_key=True)
    user_id = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE)
    status_flag = models.CharField()
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)


class User(AbstractUser):
    email = models.EmailField(max_length=255, unique=True, )
    dateofbirth = models.DateField(auto_now=False, null=True, blank=True)
    friend_id = models.ManyToManyField('self', Friend)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.username


class Posts(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    date_posted = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE)
    image = models.ImageField(upload_to="profile_pics", default='default.jpg', null=True)
    date_modified = models.DateTimeField(auto_now=True, blank=True)

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
