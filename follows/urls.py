from django.urls import path
from . import views

urlpatterns = [
    path(
        "follow/<int:user_id>/",
        views.follow_user,
        name="follow_user",
    ),
    path(
    "followers/<int:user_id>/",
    views.followers_list,
    name="followers_list",
),

path(
    "following/<int:user_id>/",
    views.following_list,
    name="following_list",
),
]