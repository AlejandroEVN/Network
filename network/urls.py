
from django.urls import path, re_path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),    
    path("post/add", views.new_post, name="new_post"),
    path("profile/<str:user_id>", views.user_profile, name="profile"),
    path("profile/<str:user_id>/following_list", views.following_list, name="following"),

    # Paths for AJAX calls

    # Edit post content
    path("edit/<str:post_id>", views.edit_post, name="edit_post"),

    # Like/unlike post
    path("like/<str:post_id>", views.like_post, name="like_post"),

    # Follow/Unfollow user
    path("profile/<str:user_id>/follow", views.toggle_follow, name="follow ")
]
