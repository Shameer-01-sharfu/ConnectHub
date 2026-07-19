from django.urls import path
from . import views


urlpatterns = [

    path(
        "",
        views.reels_feed,
        name="reels"
    ),

    path(
    "<int:reel_id>/",
    views.reel_detail,
    name="reel_detail"
),

    path(
        "create/",
        views.create_reel,
        name="create_reel"
    ),

    path(
        "like/<int:reel_id>/",
        views.like_reel,
        name="like_reel"
    ),

    path(
        "save/<int:reel_id>/",
        views.save_reel,
        name="save_reel"
    ),

    path(
    "comment/<int:reel_id>/",
    views.add_comment,
    name="reel_comment"
    ),

    path(
    "saved/",
    views.saved_reels,
    name="saved_reels"
    ),

    path(
    "edit/<int:reel_id>/",
    views.edit_reel,
    name="edit_reel"
    ),

    path(
    "delete/<int:reel_id>/",
    views.delete_reel,
    name="delete_reel"
    ),

    path(
    "share/<int:reel_id>/",
    views.share_reel,
    name="share_reel"
),

path(
    "search-users/",
    views.search_users,
    name="search_users"
),

path(
    "shared/",
    views.shared_reels,
    name="shared_reels"
),

]