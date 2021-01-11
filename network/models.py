from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


# Creates model for posts
class Post(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )
    
    timestamp = models.DateTimeField(
        auto_now_add=True
    )

    content = models.CharField(
        max_length=240
    )

    likes = models.ManyToManyField (
        User,
        blank=True,
        related_name="post_likes"
    )

    def __str__(self):
        return f"User: {self.user} posted the post '{self.content}' on {self.timestamp}"

    def serialize(self):
        return {
            "id": self.id,
            "user": self.user.username,
            "user_id": self.user.id,
            "timestamp": self.timestamp.strftime("%b %d %Y, %I:%M %p"),
            "content": self.content,
            "likes": self.likes.all().count()
        }


# User profile model
class Profile(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    followers = models.ManyToManyField(
        User,
        default=0,
        related_name="profile_followers"
    )

    following = models.ManyToManyField(
        User,
        default=0,
        related_name="profile_following"
    )

    def serialize(self):
        return {
            "user": self.user,
            "following_list": self.following,
            "followers_list": self.followers
        }

    def __str__(self):
        return f"Profile: {self.user}"