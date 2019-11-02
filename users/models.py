from django.db import models
from PIL import Image
from django.utils.text import slugify
from django_project.settings import AUTH_USER_MODEL


class Profile(models.Model):
    """docstring for Profile"""
    user = models.OneToOneField(AUTH_USER_MODEL, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to="profile_pics")
    date_modified = models.DateTimeField(auto_now=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    slug = models.SlugField(max_length=250, null=True, blank=True)

    def _get_unique_slug(self):
        slug = slugify(self.label)
        unique_slug = slug
        num = 1
        while Profile.objects.filter(slug=unique_slug).exists():
            unique_slug = '{}-{}'.format(slug, num)
            num += 1
        return unique_slug

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self._get_unique_slug()
        super(Profile, self).save(*args, **kwargs)

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


class FriendRequest(models.Model):
    to_user = models.ForeignKey(AUTH_USER_MODEL, related_name='to_user', on_delete=models.CASCADE)
    from_user = models.ForeignKey(AUTH_USER_MODEL, related_name='from_user', on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True) # set when created

    def __str__(self):
        return "From {}, to {}".format(self.from_user.username, self.to_user.username)

