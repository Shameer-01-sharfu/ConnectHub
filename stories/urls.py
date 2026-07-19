from django.urls import path
from . import views

urlpatterns = [
    path(
        "upload/",
        views.upload_story,
        name="upload_story",
    ),

    path(
        "user/<int:user_id>/",
        views.user_stories,
        name="user_stories",
    ),

    path(
    "highlight/create/",
    views.create_highlight,
    name="create_highlight",
),

path(
    "highlight/add/<int:story_id>/",
    views.add_story_to_highlight,
    name="add_story_to_highlight",
),

path(
    "highlight/<int:highlight_id>/",
    views.view_highlight,
    name="view_highlight",
),

path(
    "react/<int:story_id>/<str:emoji>/",
    views.react_story,
    name="react_story",
),
]