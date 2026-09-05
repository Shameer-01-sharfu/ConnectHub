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

    # ---------------------------
    # Video / Audio Calls
    # ---------------------------

    path(
        "call/start/<int:user_id>/",
        views.call_start,
        name="call_start"
    ),

    path(
        "call/<int:call_id>/",
        views.call_page,
        name="call_page"
    ),

    path(
        "call/<int:call_id>/offer/",
        views.call_offer,
        name="call_offer"
    ),

    path(
        "call/<int:call_id>/answer/",
        views.call_answer,
        name="call_answer"
    ),

    path(
        "call/<int:call_id>/ice/",
        views.call_ice,
        name="call_ice"
    ),

    path(
        "call/<int:call_id>/status/",
        views.call_status,
        name="call_status"
    ),

    path(
        "call/<int:call_id>/reject/",
        views.call_reject,
        name="call_reject"
    ),

    path(
        "call/<int:call_id>/end/",
        views.call_end,
        name="call_end"
    ),

    path(
        "call/incoming/",
        views.call_incoming,
        name="call_incoming"
    ),


]