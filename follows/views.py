from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Follow
from django.contrib.auth.models import User
from notifications.models import Notification
from django.shortcuts import render


@login_required
def follow_user(request, user_id):

    user_to_follow = get_object_or_404(User, id=user_id)

    if request.user != user_to_follow:

        follow = Follow.objects.filter(
            follower=request.user,
            following=user_to_follow
        )

        if follow.exists():

            follow.delete()

        else:

            Follow.objects.create(
                follower=request.user,
                following=user_to_follow
            )

            Notification.objects.create(
                receiver=user_to_follow,
                sender=request.user,
                message=f"{request.user.username} started following you."
            )

    return redirect("home")


def followers_list(request, user_id):

    profile_user = get_object_or_404(User, id=user_id)

    followers = Follow.objects.filter(
        following=profile_user
    )

    return render(
        request,
        "follows/followers.html",
        {
            "profile_user": profile_user,
            "followers": followers,
        },
    )


def following_list(request, user_id):

    profile_user = get_object_or_404(User, id=user_id)

    following = Follow.objects.filter(
        follower=profile_user
    )

    return render(
        request,
        "follows/following.html",
        {
            "profile_user": profile_user,
            "following": following,
        },
    )

