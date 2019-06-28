from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from PIL import Image


class Post(models.Model):
    title = models.CharField(max_length=100)
    image = models.ImageField(upload_to='blog_image', default='default.jpg')
    likes = models.ManyToManyField(User, related_name='likes', blank=True)
    smallContent = models.TextField()
    content = models.TextField()
    data_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    def total_likes(self):
        return self.likes.count()

    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'id': self.pk})


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    reply = models.ForeignKey('self', null=True, related_name='replies', on_delete=models.CASCADE)
    content = models.TextField(max_length=200)
    timeStamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '{}-{}'.format(str(self.user.username), self.post.title)


class PhoneType(models.Model):
    page = models.CharField(max_length=20)
    title = models.CharField(max_length=50)
    image = models.ImageField(upload_to='phone_type')