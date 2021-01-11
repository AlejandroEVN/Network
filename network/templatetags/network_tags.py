from django import template

from network.models import User, Post, Profile
from network.util import get_profile

register = template.Library()

"""
Template tags used in posts_template.html
"""

# Check if the logged user likes the post
@register.simple_tag
def is_liked(user, post_id):
    liked = Post.objects.get(pk=post_id).likes.filter(id=user)

    if len(liked) == 0:
        return False
    else:
        return True

# Checks if the logged user follows another user
@register.simple_tag
def is_followed(user, profile):
    if user in profile.followers.all():
        return True
    else:
        return False