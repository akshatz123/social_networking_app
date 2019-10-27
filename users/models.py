from django.db import models
from django.contrib.auth.models import User
from PIL import Image


class Profile(models.Model):
	"""docstring for Profile"""
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	image = models.ImageField(default='default.jpg', upload_to='profile_pics')
	mobile_number = models.IntegerField(default=0, blank=True)
	
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