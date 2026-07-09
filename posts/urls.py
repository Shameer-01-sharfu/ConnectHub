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

]