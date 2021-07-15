from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.fields.related import ForeignKey


class User(AbstractUser):
    pass

class Like(models.Model):
    user = ForeignKey(User, on_delete=models.CASCADE, related_name="user_likes")
    post = ForeignKey('Post', on_delete=models.CASCADE, related_name="post")

class Follow(models.Model):
    user = ForeignKey(User, on_delete=models.CASCADE, related_name="followers")
    following = ForeignKey(User, on_delete=models.CASCADE, related_name="following")

    def __str__(self):
        return f"{self.user} follows {self.following}"
    
    def serialize(self):
        return {
            "id": self.id,
            "user": self.user.username,
            "following": self.following.username
        }

class Post(models.Model):
    poster = ForeignKey(User, on_delete=models.CASCADE, related_name="creator_of_post")
    content = models.TextField(max_length=256)
    created = models.DateTimeField(auto_now_add=True)
    likes = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.poster}: {self.content}"
    
    def serialize(self):
        return {
            "id": self.id,
            "poster": self.poster.username,
            "content": self.content,
            "created": self.created.strftime("%b %d %Y, %I:%M %p"),
            "likes": self.likes
        }