from django.urls import path
from . import views

urlpatterns = [

    path(
        "",
        views.chats,
        name="chats",
    ),

    path(
        "<int:user_id>/",
        views.chat,
        name="chat",
    ),

    path(
        "typing/",
        views.typing_status,
        name="typing_status"
    ),

    path(
        "check-typing/<int:user_id>/",
        views.check_typing,
        name="check_typing"
    ),
    path(
    "messages/<int:user_id>/",
    views.get_messages,
    name="get_messages",
    ),
    path(
    "list-refresh/",
    views.chat_list_refresh,
    name="chat_list_refresh"
    ),
    path(
    "delete-message/<int:message_id>/",
    views.delete_message,
    name="delete_message",
),


]