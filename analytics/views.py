from django.shortcuts import render
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.models import User
from django.db.models import Count
from datetime import timedelta
from django.utils import timezone

from posts.models import Post
from reels.models import Reel
from chat.models import Message
from notifications.models import Notification


@staff_member_required
def admin_analytics(request):

    today = timezone.now().date()

    dates = []
    user_counts = []

    for i in range(6, -1, -1):

        day = today - timedelta(days=i)

        dates.append(day.strftime("%d %b"))

        count = User.objects.filter(
            date_joined__date=day
        ).count()

        user_counts.append(count)

    context = {

        "users": User.objects.count(),

        "posts": Post.objects.count(),

        "reels": Reel.objects.count(),

        "total_messages": Message.objects.count(),

        "notifications": Notification.objects.count(),

        "recent_users": User.objects.order_by("-date_joined")[:10],

        "top_reels": Reel.objects.annotate(
            total_likes=Count("likes")
        ).select_related("user").order_by("-total_likes")[:5],

        "top_users": User.objects.annotate(
            total_posts=Count("posts")
        ).order_by("-total_posts")[:5],

        "top_posts": Post.objects.annotate(
    total_likes=Count("likes")
).select_related("user").order_by("-total_likes")[:5],

        "dates": dates,

        "user_counts": user_counts,

    }

    return render(
        request,
        "analytics/dashboard.html",
        context
    )