from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage, InvalidPage

from .models import User, Post, Profile


# Helper to paginate query sets passed from views.py
def paginate_posts(queryset, page):
    per_page = 10
    paginator = Paginator(queryset, per_page)

    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

    return posts


# Helper to get the requested user profile
def get_profile(user_id):
    try:
        profile = Profile.objects.get(user=user_id)
    except ObjectDoesNotExist:
        return 404

    return profile