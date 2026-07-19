from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from .forms import RegisterForm, ProfileUpdateForm
from posts.models import Post
from stories.models import Story
from django.utils import timezone

from follows.models import Follow
from django.db.models import Max
from stories.models import Highlight
from posts.models import SavedPost
def home(request):

    users = []
    following_ids = []
    stories = []
    saved_posts = []
    posts = Post.objects.all().select_related("user").prefetch_related(
        "likes",
        "comments"
    ).order_by("-created_at")

    highlights = Highlight.objects.none()

    if request.user.is_authenticated:

        highlights = Highlight.objects.exclude(
            user=request.user
        ).order_by("-created_at")

        users = User.objects.exclude(id=request.user.id)

        following_ids = Follow.objects.filter(
            follower=request.user
        ).values_list(
            "following_id",
            flat=True
        )

        saved_posts = SavedPost.objects.filter(
    user=request.user
).values_list(
    "post_id",
    flat=True
)

        latest_story_users = (
            Story.objects.filter(
                expires_at__gt=timezone.now()
            )
            .values("user")
            .annotate(last_story=Max("created_at"))
        )

        stories = []

        for item in latest_story_users:

            latest_story = Story.objects.filter(
                user=item["user"],
                expires_at__gt=timezone.now()
            ).order_by("-created_at").first()

            if latest_story:
                stories.append(latest_story)

    return render(
        request,
        "accounts/home.html",
        {
            "users": users,
            "following_ids": following_ids,
            "stories": stories,
            "highlights": highlights,
            "posts": posts,
            "saved_posts": saved_posts,
        }
    )


def register(request):
    if request.user.is_authenticated:
        return redirect("home")

    if request.method == "POST":
        form = RegisterForm(request.POST)

        if form.is_valid():
            user = form.save()

            messages.success(
                request,
                "🎉 Registration successful! Please login."
            )

            return redirect("login")

    else:
        form = RegisterForm()

    return render(
        request,
        "accounts/register.html",
        {
            "form": form
        }
    )


def login_user(request):

    if request.user.is_authenticated:
        return redirect("home")

    if request.method == "POST":

        form = AuthenticationForm(request, data=request.POST)

        if form.is_valid():

            username = form.cleaned_data.get("username")

            password = form.cleaned_data.get("password")

            user = authenticate(
                username=username,
                password=password
            )

            if user:

                login(request, user)

                messages.success(
                    request,
                    f"Welcome {user.username} 👋"
                )

                return redirect("home")

    else:

        form = AuthenticationForm()

    return render(
        request,
        "accounts/login.html",
        {
            "form": form
        }
    )


def logout_user(request):

    logout(request)

    messages.success(
        request,
        "Logged out successfully."
    )

    return redirect("login")

from django.contrib.auth.decorators import login_required


from django.contrib.auth.decorators import login_required

@login_required
def profile(request):

    profile = request.user.profile

    highlights = Highlight.objects.filter(
        user=request.user
    )

    stories = Story.objects.filter(
        user=request.user
    ).order_by("-created_at")

    if request.method == "POST":

        form = ProfileUpdateForm(
            request.POST,
            request.FILES,
            instance=profile
        )

        if form.is_valid():

            form.save()

            messages.success(
                request,
                "Profile Updated Successfully."
            )

            return redirect("profile")

    else:

        form = ProfileUpdateForm(
            instance=profile
        )

    return render(
        request,
        "accounts/profile.html",
        {
            "form": form,
            "profile": profile,
            "highlights": highlights,
            "stories": stories,
        },
    )

def user_profile(request, user_id):

    profile_user = get_object_or_404(
        User,
        id=user_id
    )

    # User Posts
    posts = Post.objects.filter(
        user=profile_user
    )

    # User Highlights
    highlights = Highlight.objects.filter(
        user=profile_user
    ).order_by("-created_at")

    is_following = False
    can_message = False

    if request.user.is_authenticated:

        is_following = Follow.objects.filter(
            follower=request.user,
            following=profile_user
        ).exists()

        can_message = is_following

    context = {
        "profile_user": profile_user,
        "posts": posts,
        "highlights": highlights,
        "is_following": is_following,
        "can_message": can_message,
    }

    return render(
        request,
        "accounts/user_profile.html",
        context,
    )
