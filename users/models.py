from django.db import models
from django.contrib.auth.models import User
from PIL import Image


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to='user_profile')

    def __str__(self):
        return f'{self.user.username} Profile'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        img = Image.open(self.image.path)

        if img.width > 300 or img.height > 300:
            output_img = (400, 400)
            img.thumbnail(output_img)
            img.save(self.image.path)


class AddLike(models.Model):
    add_name = models.CharField(max_length=50)
    add_like = models.ManyToManyField(User, blank=True, related_name='add_likes')
