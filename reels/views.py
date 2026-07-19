from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.contrib.auth.models import User

from .models import Reel, ReelComment, ReelShare
from .forms import ReelForm, ReelCommentForm

from chat.models import Message
from notifications.utils import create_notification


# ==========================
# CREATE REEL
# ==========================

@login_required
def create_reel(request):

    if request.method == "POST":

        form = ReelForm(request.POST, request.FILES)

        if form.is_valid():

            reel = form.save(commit=False)

            reel.user = request.user

            reel.save()

            messages.success(
                request,
                "Reel uploaded successfully."
            )

            return redirect("reels")

    else:

        form = ReelForm()

    return render(

        request,

        "reels/create_reel.html",

        {

            "form": form

        }

    )


# ==========================
# REELS FEED
# ==========================

@login_required
def reels_feed(request):

    reels = Reel.objects.all().prefetch_related(

        "likes",

        "comments",

        "saved_by"

    )

    for reel in reels:

        reel.is_saved = reel.saved_by.filter(

            id=request.user.id

        ).exists()

        if request.user not in reel.views.all():
          reel.views.add(request.user)

    return render(

        request,

        "reels/reels_feed.html",

        {

            "reels": reels,

            "comment_form": ReelCommentForm()

        }

    )


# ==========================
# LIKE REEL
# ==========================

@login_required
def like_reel(request, reel_id):

    reel = get_object_or_404(

        Reel,

        id=reel_id

    )

    user = request.user

    if user in reel.likes.all():

        reel.likes.remove(user)

        liked = False

    else:

        reel.likes.add(user)

        create_notification(

            receiver=reel.user,

            sender=request.user,

            message=f"{request.user.username} liked your reel ❤️",

            link="/reels/"

        )

        liked = True

    return JsonResponse({

        "liked": liked,

        "likes_count": reel.likes.count()

    })
# ==========================
# SAVE REEL
# ==========================

@login_required
def save_reel(request, reel_id):

    reel = get_object_or_404(

        Reel,

        id=reel_id

    )

    if request.user in reel.saved_by.all():

        reel.saved_by.remove(request.user)

        saved = False

    else:

        reel.saved_by.add(request.user)

        saved = True

    if request.headers.get("x-requested-with") == "XMLHttpRequest":

        return JsonResponse({

            "saved": saved

        })

    return redirect("reels")


# ==========================
# ADD COMMENT
# ==========================

@login_required
def add_comment(request, reel_id):

    reel = get_object_or_404(

        Reel,

        id=reel_id

    )

    if request.method == "POST":

        form = ReelCommentForm(request.POST)

        if form.is_valid():

            comment = form.save(commit=False)

            comment.user = request.user

            comment.reel = reel

            comment.save()

            create_notification(

                receiver=reel.user,

                sender=request.user,

                message=f"{request.user.username} commented on your reel 💬",

                link="/reels/"

            )

            messages.success(

                request,

                "Comment added."

            )

            return redirect("reels")

    else:

        form = ReelCommentForm()

    return render(

        request,

        "reels/comment.html",

        {

            "reel": reel,

            "form": form

        }

    )


# ==========================
# SAVED REELS
# ==========================

@login_required
def saved_reels(request):

    reels = Reel.objects.filter(

        saved_by=request.user

    ).prefetch_related(

        "likes",

        "comments",

        "saved_by"

    )

    return render(

        request,

        "reels/saved_reels.html",

        {

            "reels": reels

        }

    )
# ==========================
# EDIT REEL
# ==========================

@login_required
def edit_reel(request, reel_id):

    reel = get_object_or_404(

        Reel,

        id=reel_id,

        user=request.user

    )

    if request.method == "POST":

        form = ReelForm(

            request.POST,

            request.FILES,

            instance=reel

        )

        if form.is_valid():

            form.save()

            messages.success(

                request,

                "Reel updated successfully."

            )

            return redirect("reels")

    else:

        form = ReelForm(instance=reel)

    return render(

        request,

        "reels/edit_reel.html",

        {

            "form": form,

            "reel": reel

        }

    )


# ==========================
# DELETE REEL
# ==========================

@login_required
def delete_reel(request, reel_id):

    reel = get_object_or_404(

        Reel,

        id=reel_id,

        user=request.user

    )

    if request.method == "POST":

        reel.delete()

        messages.success(

            request,

            "Reel deleted successfully."

        )

        return redirect("reels")

    return render(

        request,

        "reels/delete_reel.html",

        {

            "reel": reel

        }

    )


# ==========================
# SEARCH USERS
# ==========================

@login_required
def search_users(request):

    query = request.GET.get("q", "")

    users = User.objects.filter(

        username__icontains=query

    ).exclude(

        id=request.user.id

    )[:10]

    data = []

    for user in users:

        data.append({

            "id": user.id,

            "username": user.username,

            "name": f"{user.first_name} {user.last_name}"

        })

    return JsonResponse(data, safe=False)


# ==========================
# SHARE REEL
# ==========================

@login_required
def share_reel(request, reel_id):

    if request.method == "POST":

        receiver = get_object_or_404(

            User,

            id=request.POST.get("receiver")

        )

        # Send reel in chat
        Message.objects.create(

            sender=request.user,

            receiver=receiver,

            message=f"[REEL]{reel_id}"

        )

        # Notification
        create_notification(

            receiver=receiver,

            sender=request.user,

            message=f"{request.user.username} shared a reel with you 🎥",

            link=f"/chat/{request.user.id}/"

        )

        return JsonResponse({

            "success": True

        })

    return JsonResponse({

        "success": False

    })


# ==========================
# SHARED REELS
# ==========================

@login_required
def shared_reels(request):

    shares = ReelShare.objects.filter(

        receiver=request.user

    ).select_related(

        "sender",

        "reel"

    )

    return render(

        request,

        "reels/shared_reels.html",

        {

            "shares": shares

        }

    )
@login_required
def reel_detail(request,reel_id):

    reel=get_object_or_404(
        Reel,
        id=reel_id
    )

    return render(
        request,
        "reels/reel_detail.html",
        {
            "reel":reel
        }
    )