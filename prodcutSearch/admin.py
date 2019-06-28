from django.contrib import admin
from .models import Post, Comment
from .models import PhoneType


admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(PhoneType)


