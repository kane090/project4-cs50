from django.contrib import admin
from .models import Follow, User, Post

# Register your models here.
admin.site.register(Post)
admin.site.register(User)
admin.site.register(Follow)