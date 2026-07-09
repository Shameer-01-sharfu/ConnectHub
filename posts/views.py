from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .forms import PostForm


@login_required
def create_post(request):

    if request.method == "POST":

        form = PostForm(
            request.POST,
            request.FILES
        )

        if form.is_valid():

            post = form.save(commit=False)

            post.user = request.user

            post.save()

            messages.success(
                request,
                "Post Created Successfully."
            )

            return redirect("feed")

    else:

        form = PostForm()

    return render(
        request,
        "posts/create_post.html",
        {
            "form": form
        }
    )


@login_required
def feed(request):

    from .models import Post

    posts = Post.objects.all()

    return render(
        request,
        "posts/feed.html",
        {
            "posts": posts
        }
    )