from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages

from .forms import RegisterForm, ProfileUpdateForm
from posts.models import Post


def home(request):

    if request.user.is_authenticated:

        posts_count = Post.objects.filter(
            user=request.user
        ).count()

        context = {
            "posts_count": posts_count,
            "followers_count": 0,
            "following_count": 0,
        }

        return render(
            request,
            "accounts/home.html",
            context
        )

    return render(
        request,
        "accounts/home.html"
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

    if request.method == "POST":
        form = ProfileUpdateForm(
            request.POST,
            request.FILES,
            instance=profile
        )

        if form.is_valid():
            form.save()
            messages.success(request, "Profile Updated Successfully.")
            return redirect("profile")

    else:
        form = ProfileUpdateForm(instance=profile)

    return render(
        request,
        "accounts/profile.html",
        {
            "form": form,
            "profile": profile,
        },
    )