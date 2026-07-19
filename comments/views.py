from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

from posts.models import Post
from .models import Comment
from .forms import CommentForm
from django.http import JsonResponse

@login_required
def add_comment(request, post_id):

    post = get_object_or_404(Post, id=post_id)

    if request.method == "POST":

        form = CommentForm(request.POST)

        if form.is_valid():

            comment = form.save(commit=False)

            comment.user = request.user

            comment.post = post

            comment.save()

            return JsonResponse({

                "success": True,

                "username": request.user.username,

                "comment": comment.comment,

                "comments_count": post.comments.count(),

            })

    return JsonResponse({"success": False}, status=400)