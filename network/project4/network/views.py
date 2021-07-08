import json

from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse

from .models import Follow, User, Post


def index(request):
    return render(request, "network/index.html", {
        "posts": Post.objects.all().order_by('id').reverse()
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
                "message": "Invalid username and/or password."
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
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")


def new_post(request):
    if request.method == "POST":
        poster = request.user
        content = request.POST["content"]
        Post.objects.create(poster=poster, content=content)
        return HttpResponseRedirect(reverse("index"))

def profile(request, user):
    profile_to_view = User.objects.get(username=user)
    posts = Post.objects.filter(poster=profile_to_view)
    followers = Follow.objects.filter(following=profile_to_view).count()
    following = Follow.objects.filter(user=profile_to_view).count()
    return render(request, "network/profile.html", {
        "profile": profile_to_view,
        "posts": posts,
        "followers": followers,
        "following": following
    })

def follow(request, user):
    user_to_follow = User.objects.get(username=user)
    current_user = request.user
    follow_object = Follow(user=current_user, following=user_to_follow)
    follow_object.save()
    return HttpResponseRedirect(reverse("profile", args=[user]))

def following(request, user):
    pass