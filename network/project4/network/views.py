import json

from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse

from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator
from django.views.decorators.csrf import csrf_exempt

from .models import Follow, User, Post


def index(request, page_number):
    posts = Post.objects.all().order_by('id').reverse()
    p = Paginator(posts, 10)
    current_page = p.page(page_number)
    return render(request, "network/index.html", {
        "current_page": current_page,
        "following": False,
        "page_number": page_number,
        "page_range": p.page_range
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
            return HttpResponseRedirect(reverse("index", args=[1]))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index", args=[1]))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index", args=[1]))
    else:
        return render(request, "network/register.html")


def new_post(request):
    if request.method == "POST":
        poster = request.user
        content = request.POST["content"]
        Post.objects.create(poster=poster, content=content)
        return HttpResponseRedirect(reverse("index", args=[1]))


def profile(request, user, page_number):
    profile_to_view = User.objects.get(username=user)
    posts = Post.objects.filter(poster=profile_to_view)
    p = Paginator(posts, 10)
    current_page = p.page(page_number)
    followers = Follow.objects.filter(following=profile_to_view).count()
    following = Follow.objects.filter(user=profile_to_view).count()
    try:
        is_following = Follow.objects.get(user=request.user, following=profile_to_view)
    except (ObjectDoesNotExist, TypeError):
        is_following = None
    return render(request, "network/profile.html", {
        "profile": profile_to_view,
        "current_page": current_page,
        "followers": followers,
        "following": following,
        "is_following": is_following,
        "page_number": page_number,
        "page_range": p.page_range
    })


def follow(request, user):
    user_to_follow = User.objects.get(username=user)
    current_user = request.user
    try:
        existing_follow_object = Follow.objects.get(user=request.user, following=user_to_follow)
    except ObjectDoesNotExist:
        existing_follow_object = None
    if existing_follow_object:
        existing_follow_object.delete()
    else:
        follow_object = Follow(user=current_user, following=user_to_follow)
        follow_object.save()
    return HttpResponseRedirect(reverse("profile", args=[user, 1]))


def following(request, page_number):
    following_objects = Follow.objects.filter(user=request.user)
    users_following = [follow.following for follow in following_objects]
    all_posts = Post.objects.all().order_by('id').reverse()
    following_posts = [post for post in all_posts if post.poster in users_following]
    p = Paginator(following_posts, 10)
    current_page = p.page(page_number)
    return render(request, "network/index.html", {
        "current_page": current_page,
        "following": True,
        "page_number": page_number,
        "page_range": p.page_range
    })

@csrf_exempt
def edit(request, post_id):
    post = Post.objects.get(pk=post_id)
    if request.method == "PUT":
        data = json.loads(request.body)
        content_to_save = data.get("content")
        if post.content != content_to_save:
            post.content = content_to_save
            post.save()
    return HttpResponse(status=204)


def like(request, post_id):
    pass