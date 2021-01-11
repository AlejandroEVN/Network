from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator, InvalidPage, EmptyPage, PageNotAnInteger
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt

from .models import User, Post, Profile
from .forms import PostForm
from .util import paginate_posts, get_profile

import json


# Error messages
USER_NOT_FOUND = 'This user does not exist !'
INVALID_CREDENTIALS = 'Invalid username and/or password!'
PASSWORDS_DONT_MATCH = 'Passwords must match !'
EXISTING_USER = 'Username already taken !'

# Homepage
def index(request):
    
    # Create new post form
    post_form = PostForm()

    # Get all the posts in the db by reverse chronological order
    posts = Post.objects.all().order_by("-timestamp")

    # Gets the requested page (page 1 by default)
    page = request.GET.get('page', 1)

    # Paginates the posts list
    posts = paginate_posts(posts, page)
    
    return render(request, "network/index.html", {
        "post_form": post_form,
        "posts": posts
    })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": INVALID_CREDENTIALS
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": PASSWORDS_DONT_MATCH
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": EXISTING_USER
            })
        login(request, user)

        # Gets the created user and creates a profile for the new user
        user = User.objects.get(username=username)
        new_profile = Profile(user=user)
        new_profile.save()

        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")


@login_required
def new_post(request):
    if request.method == "POST":

        # Create a post form and populate it with the submitted data
        post_form = PostForm(request.POST)

        # Check if the form is valid
        if post_form.is_valid():

            # Get the content of the new post
            content = post_form.cleaned_data["content"]

            # Save the post into the db
            new_post = Post(user=request.user, content=content)
            new_post.save()

            # Redirect to index page
            return HttpResponseRedirect(reverse('index'))


@login_required
def user_profile(request, user_id):

    # Gets the profile and the posts of the targeted user
    profile = get_profile(user_id)

    if profile == 404:
        return render(request, 'network/profile.html', {
            'message': USER_NOT_FOUND
        })

    # Gets posts from the requested user
    user_posts = Post.objects.filter(user=user_id).order_by('-timestamp')

    # Page requested. First page by default
    page = request.GET.get('page', 1)

    # Paginate user posts
    posts = paginate_posts(user_posts, page)

    return render(request, 'network/profile.html', {
        'profile': profile,
        'posts': posts
    })


@login_required
def following_list(request, user_id):

    # Gets the profile of the requested user
    target_profile = get_profile(user_id)

    # Return alert if the profile wasn't found
    if target_profile == 404:
        return render(request, 'network/profile.html', {
            'message': USER_NOT_FOUND
        })

    # Gets the user's following list
    target_profile_following = target_profile.following.all()

    # Gets the posts from the user's following list
    following_posts = Post.objects.filter(
        user__in=target_profile_following
        )
    following_posts = following_posts.order_by('-timestamp')

    # Page requested. First by default
    page = request.GET.get('page', 1)

    # Paginate the posts list
    posts = paginate_posts(following_posts, page)

    return render(request, 'network/following.html', {
        'profile': target_profile,
        'posts': posts
    })


# Sets follow/unfollow
@login_required
@csrf_exempt
def toggle_follow(request, user_id):
    if request.method == "PUT":
        try:
             
            # Gets the profile of the user to follow/unfollow
            target_user = get_profile(user_id)

            # Gets the requesting user
            req_user_profile = get_profile(request.user.id)

            # Return alert if either profiles weren't found
            if target_user == 404 or req_user_profile == 404:
                return render(request, 'network/profile.html', {
                    'message': USER_NOT_FOUND
                })

            # If the user is already following the targeted user
            if req_user_profile.user in target_user.followers.all():

                # Unfollow the targeted user
                target_user.followers.remove(req_user_profile.user)

                # Removes the targeted user from the requesting users'
                # following list
                req_user_profile.following.remove(target_user.user)

                following = False
            else:

                # Follow the targeted user
                target_user.followers.add(req_user_profile.user)

                # Adds the targeted user from the requesting users'
                # following list
                req_user_profile.following.add(target_user.user)
                
                following = True

            # Data to send back to the front end
            updated_follow = {
                "followers": target_user.followers.all().count(),
                "following": following
            }
                
        # If the targeted user doesn't exist show an alert
        except ObjectDoesNotExist:
            return render(request, 'network/profile.html', {
                'message': USER_NOT_FOUND
            })

        return JsonResponse(updated_follow, safe=False)
    else:        
        return JsonResponse(["Unauthorized"], safe=False)


# Sets post liked
@login_required
@csrf_exempt
def like_post(request, post_id, string=None, user_id=None):
    
    # Checks for correct request method
    if request.method == "PUT":

        # Gets the content passed by the ajax request
        data = json.loads(request.body)

        # Gets whether the post is liked by the user or not
        liked = data.get("liked")

        # Gets the post that needs to be liked/unliked
        post = Post.objects.get(pk=post_id)

        # If the post is liked, remove user from the likes list
        # else, adds the user to the likes list
        if liked:
            post.likes.remove(request.user)
            liked = False
        else:
            post.likes.add(request.user)
            liked = True

        # Data to send back to the front end
        updated_likes = {
            "liked": liked,
            "post_likes": post.likes.all().count()
        }

        return JsonResponse(updated_likes, safe=False)
    else:
        return JsonResponse(["Unauthorized"], safe=False)


# Edits the content of the post
@login_required
@csrf_exempt
def edit_post(request, post_id, string=None):
    
    # Checks for correct request method
    if request.method == "PUT":

        # Gets the content passed by the ajax request
        data = json.loads(request.body)

        # Creates dict to store the values to update in the Post model
        update_data = {
            "content": data.get("content", "")
        }

        # Selects the requested post to update and updates it's value  
        edit_post = Post.objects.filter(pk=post_id)
        edit_post.update(**update_data)

        # Returns the updated content
        return JsonResponse(edit_post.first().content, safe=False)
    else:
        return JsonResponse(["Unauthorized"], safe=False)