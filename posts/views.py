from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .forms import PostForm
from django.shortcuts import get_object_or_404
from .models import Post
from django.views.decorators.http import require_POST
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

@require_POST
@login_required
def like_post(request, post_id):

    post = get_object_or_404(Post, id=post_id)

    if request.user in post.likes.all():

        post.likes.remove(request.user)

    else:

        post.likes.add(request.user)

    return redirect("feed")