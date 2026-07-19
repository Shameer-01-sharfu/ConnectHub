from django.urls import path
from . import views

urlpatterns = [

    path(
        "create/",
        views.create_post,
        name="create_post"
    ),

    path(
        "feed/",
        views.feed,
        name="feed"
    ),

    path(
        "like/<int:post_id>/",
        views.like_post,
        name="like_post"
    ),

    path(
    "comment/<int:post_id>/",
    views.add_comment,
    name="add_comment"
    ),

    path(
    "edit/<int:post_id>/",
    views.edit_post,
    name="edit_post"
    ),

    path(
    "delete/<int:post_id>/",
    views.delete_post,
    name="delete_post"
    ),

    path(
    "save/<int:post_id>/",
    views.save_post,
    name="save_post"
    ),

    path(
    "saved/",
    views.saved_posts,
    name="saved_posts"
    ),

    path(
    "share/<int:post_id>/",
    views.share_post,
    name="share_post"
),

]