import json
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, redirect
from django.urls import reverse
from django import forms
from django.core.paginator import Paginator
from .models import *


class CreatePostForm(forms.ModelForm):
    """
    Form for creating a new post
    """
    class Meta:
        # Define the model and fields to be used in the form
        model = Post
        fields = ['content']
        widgets = {'content': forms.Textarea(attrs={'class': 'form-control mb-3'})}

    def __init__(self, *args, **kwargs):
        """
        Initialize the form and set placeholders for each field.
        """
        super().__init__(*args, **kwargs)
        # Set the placeholder and label for each field
        for _, field in self.fields.items():
            field.widget.attrs['placeholder'] = ""
            field.label = ""


def index(request):
    """
    View function for the index page.
    Displays all posts in reverse chronological order.
    """
    # Get all posts ordered by creation date
    posts_list = Post.objects.all().order_by("-created_at")
    
    # Get the posts for the index page
    paginator = Paginator(posts_list, 10)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)
    
    return render(request, "network/index.html", {
        "active_filter": "all",
        "show_profile": False,
        "posts": page_obj,
        "page_obj": page_obj,
        "owner": None,
    })


@login_required
def following(request):
    """
    View function for the following page.
    Displays posts from users that the current user is following.
    """
    # Get the list of users that the current user is following
    if request.user.is_authenticated:
        following_users = Follow.objects.filter(follower=request.user).values_list('followed', flat=True)
        posts_list = Post.objects.filter(user__in=following_users).order_by("-created_at")
    else:
        posts_list = []
    
    # Get the posts for the following users
    paginator = Paginator(posts_list, 10)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)
    
    return render(request, "network/index.html", {
        "active_filter": "following",
        "show_profile": False,
        "posts": page_obj,
        "page_obj": page_obj,
        "owner": None,
    })


def profile(request, user_id):
    """
    View function for the user profile page.
    Displays the user's posts and profile information.
    """
    # Get the user object for the profile
    owner = User.objects.get(id=user_id)
    posts_list = Post.objects.filter(user=owner).order_by("-created_at")
    followers = Follow.objects.filter(followed=owner).count()
    following = Follow.objects.filter(follower=owner).count()
    is_following = request.user.is_following(owner) if request.user.is_authenticated else False

    # Get the posts for the profile
    paginator = Paginator(posts_list, 10)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)

    # Determine the active filter based on the user ID
    if request.user.id == user_id:
        active_filter = "profile"
    else:
        active_filter = "other"

    return render(request, "network/index.html", {
        "active_filter": active_filter,
        "show_profile": True,
        "posts": page_obj,
        "page_obj": page_obj,
        "owner": owner,
        "followers": followers,
        "following": following,
        "is_following": is_following
    })


@login_required
def create(request, error_message=None):
    """
    View function for creating a new post.
    Displays a form for creating a new post.
    """
    # If the request is a GET request, display the form
    if request.method == "GET":
        form = CreatePostForm()    
        return render(request, "network/create.html", {
            "post_form": form,
            "active_filter": "new"
        })

    # If the request is a POST request, process the form    
    elif request.method == "POST":
        form = CreatePostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            return redirect(reverse("index"))
        else:
            return render(request, "network/create.html", {
                "post_form": form,
                "active_filter": "new",
                "error_message": error_message
            })

    return JsonResponse({"error": "Invalid request method."}, status=400)


@csrf_exempt
@login_required
def follow(request):
    """
    View function for following or unfollowing a user.
    Handles AJAX requests to follow or unfollow a user.
    """
    if request.method == "PUT":
        # Get the user ID from the request body
        data = json.loads(request.body)
        user_id = data.get("user_id")

        # Get the user to follow
        user_to_follow = User.objects.get(id=user_id)

        if request.user.is_following(user_to_follow):
            # If already following, unfollow the user
            Follow.objects.filter(follower=request.user, followed=user_to_follow).delete()
            label = "Follow"
        else:
            # If not following, follow the user
            Follow.objects.create(follower=request.user, followed=user_to_follow)
            label = "Unfollow"

        # Get the updated followers count
        followers_count = Follow.objects.filter(followed=user_to_follow).count()

        # return the new label and followers count to display on the page
        return JsonResponse(
            {
                "message": "User followed successfully.",
                "label": label,
                "followers_count": followers_count
            }, 
            status=201
        )
    
    return JsonResponse({"error": "Invalid request method."}, status=400)


@csrf_exempt
@login_required
def like_post(request):
    """
    View function for liking or unliking a post.
    Handles AJAX requests to like or unlike a post.
    """
    if request.method == "PUT":
        # Get the post ID from the request body
        data = json.loads(request.body)
        post_id = data.get("post_id")

        # Get the post to like/unlike
        post = Post.objects.get(id=post_id)

        # Check if the user has already liked this post
        like_exists = Like.objects.filter(user=request.user, post=post).exists()

        if like_exists:
            # If already liked, unlike the post
            Like.objects.filter(user=request.user, post=post).delete()
            does_like = False
        else:
            # If not liked, like the post
            Like.objects.create(user=request.user, post=post)
            does_like = True

        # Get the updated likes count
        likes_count = post.get_likes_count()

        # return the new label and likes count to display on the page
        return JsonResponse(
            {
                "message": "Post liked successfully.",
                "likes_count": likes_count,
                "does_like": does_like
            }, 
            status=201
        )
    
    return JsonResponse({"error": "Invalid request method."}, status=400)


@csrf_exempt
@login_required
def update_post(request):
    """
    View function for updating a post.
    Handles AJAX requests to update a post's content.
    """
    if request.method == "PUT":

        # Get the post ID and new content from the request body
        data = json.loads(request.body)
        post_id = data.get("post_id")
        content = data.get("content")

        try:
            # Check that the post belongs to the currently logged in user
            post = Post.objects.get(id=post_id, user=request.user)
            post.content = content
            post.save()
            return JsonResponse({"message": "Post updated successfully."}, status=200)
        
        except Post.DoesNotExist:
            return JsonResponse({"error": "Post not found."}, status=404)

    return JsonResponse({"error": "Invalid request method."}, status=400)


def login_view(request):
    """
    Handle login request
    """
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
    """
    Handle logout request
    """
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    """
    Handle registration request
    """
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
