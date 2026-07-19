from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from .forms import PostForm
from django.shortcuts import get_object_or_404
from .models import Post, SavedPost
from django.views.decorators.http import require_POST
from comments.forms import CommentForm
from django.http import JsonResponse
from chat.models import Message
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

            return redirect("home")

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

    posts = Post.objects.all().order_by("-id")

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

        liked = False


    else:

        post.likes.add(request.user)

        liked = True



    return JsonResponse({

        "liked": liked,

        "likes_count": post.likes.count()

    })
from comments.models import Comment

@login_required
def add_comment(request, post_id):

    post = get_object_or_404(Post, id=post_id)

    if request.method == "POST":

        comment_text = request.POST.get("comment")

        if comment_text:

            Comment.objects.create(
                post=post,
                user=request.user,
                comment=comment_text
            )

            messages.success(
                request,
                "Comment Added Successfully."
            )

    return redirect("home")

@login_required
def edit_post(request, post_id):

    post = get_object_or_404(
        Post,
        id=post_id,
        user=request.user
    )

    if request.method == "POST":

        form = PostForm(
            request.POST,
            request.FILES,
            instance=post
        )

        if form.is_valid():

            form.save()

            messages.success(
                request,
                "Post Updated Successfully."
            )

            return redirect("feed")

    else:

        form = PostForm(instance=post)

    return render(
        request,
        "posts/edit_post.html",
        {
            "form": form
        }
    )


@login_required
def delete_post(request, post_id):

    post = get_object_or_404(
        Post,
        id=post_id,
        user=request.user
    )

    post.delete()

    messages.success(
        request,
        "Post Deleted Successfully."
    )

    return redirect("feed")

from django.shortcuts import get_object_or_404


@login_required
def save_post(request, post_id):

    post = get_object_or_404(Post, id=post_id)


    saved_post = SavedPost.objects.filter(
        user=request.user,
        post=post
    )


    if saved_post.exists():

        saved_post.delete()

        saved = False


    else:

        SavedPost.objects.create(
            user=request.user,
            post=post
        )

        saved = True



    return JsonResponse({

        "saved": saved

    })


@login_required
def saved_posts(request):

    saved_posts = SavedPost.objects.filter(
        user=request.user
    ).select_related(
        "post",
        "post__user"
    )

    return render(
        request,
        "posts/saved_posts.html",
        {
            "saved_posts": list(saved_posts),
        }
    )

@login_required
def share_post(request, post_id):

    if request.method != "POST":

        return JsonResponse({"success": False})

    post = get_object_or_404(Post, id=post_id)

    receiver_id = request.POST.get("receiver")

    receiver = get_object_or_404(User, id=receiver_id)

    Message.objects.create(

        sender=request.user,

        receiver=receiver,

        message=f"📤 Shared a post",

        shared_post=post

    )

    return JsonResponse({

        "success": True

    })