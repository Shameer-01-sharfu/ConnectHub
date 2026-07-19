from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.utils import timezone
from datetime import timedelta
from django.http import JsonResponse

import re

from follows.models import Follow
from reels.models import Reel
from .models import Message, TypingStatus
from .forms import MessageForm


# ===========================================
# REEL SHARE PREVIEW
# ===========================================

REEL_SHARE_RE = re.compile(r"^\[.*?\]\(https?://[^\s]+/reels/(\d+)/?\)$")
OLD_REEL_SHARE_RE = re.compile(r"^\[REEL\](\d+)$")


def _reel_share_preview(text):

    text = text.strip()

    # New format: [🎬 Shared a Reel](http://.../reels/9/)
    match = REEL_SHARE_RE.match(text)

    if match:
        reel = Reel.objects.filter(id=int(match.group(1))).first()
        return True, reel

    # Old format: [REEL]9
    old_match = OLD_REEL_SHARE_RE.match(text)

    if old_match:
        reel = Reel.objects.filter(id=int(old_match.group(1))).first()
        return True, reel

    return False, None

# ===========================================
# CHAT PAGE
# ===========================================

@login_required
def chat(request, user_id):

    other_user = get_object_or_404(User, id=user_id)

    # Update last seen
    request.user.profile.last_seen = timezone.now()
    request.user.profile.save()

    # Online Status
    online = False

    try:
        if timezone.now() - other_user.profile.last_seen < timedelta(minutes=2):
            online = True
    except:
        online = False

    # Prevent self chat
    if request.user == other_user:
        messages.error(request, "You cannot message yourself.")
        return redirect("home")

    # Follow check
    if not Follow.objects.filter(
        follower=request.user,
        following=other_user
    ).exists():

        messages.error(
            request,
            "Follow this user before sending messages."
        )

        return redirect(
            "user_profile",
            user_id=other_user.id
        )

    # Load Messages
    chat_messages = list(

        Message.objects.filter(

            sender__in=[request.user, other_user],

            receiver__in=[request.user, other_user]

        ).order_by("created_at")

    )

    for msg in chat_messages:

        msg.is_reel_share, msg.shared_reel = _reel_share_preview(msg.message)

        msg.is_post_share = (
            getattr(msg, "shared_post", None) is not None
        )

    # Read Receipts
    Message.objects.filter(

        sender=other_user,

        receiver=request.user,

        is_read=False

    ).update(is_read=True)

    # Send Message
    if request.method == "POST":

      form = MessageForm(request.POST)

      if form.is_valid():

        new_message = form.save(commit=False)

        new_message.sender = request.user

        new_message.receiver = other_user
        reply_id = request.POST.get("reply_to")

        if reply_id:
          reply_id = request.POST.get("reply_to")

        if reply_id:
          new_message.reply_to = Message.objects.filter(id=reply_id).first()

        new_message.save()

        new_message.save()

        # AJAX request
        if request.headers.get("X-Requested-With") == "XMLHttpRequest":

            return JsonResponse({

    "success": True,

    "message": new_message.message,

    "sender": request.user.username,

    "time": new_message.created_at.strftime("%I:%M %p"),

    

})

        return redirect("chat", user_id=other_user.id)

    else:

        form = MessageForm()

    # Conversation Sidebar
    conversation_user_ids = set(

        Message.objects.filter(

            sender=request.user

        ).values_list(
            "receiver",
            flat=True
        )

    ) | set(

        Message.objects.filter(

            receiver=request.user

        ).values_list(
            "sender",
            flat=True
        )

    )

    conversation_list = []

    for uid in conversation_user_ids:

        person = User.objects.get(id=uid)

        last_msg = Message.objects.filter(

            sender__in=[request.user, person],

            receiver__in=[request.user, person]

        ).order_by("-created_at").first()

        if last_msg:

            if getattr(last_msg, "shared_post", None):

                preview = "📷 Shared a Post"

            else:

                is_reel, _ = _reel_share_preview(last_msg.message)

                preview = (
                    "🎬 Shared a Reel"
                    if is_reel
                    else last_msg.message
                )

        else:

            preview = "No messages yet"

        conversation_list.append({

            "person": person,

            "last_message": preview,

        })

    return render(

        request,

        "chat/chat.html",

        {

            "chat_messages": chat_messages,

            "form": form,

            "other_user": other_user,

            "conversation_list": conversation_list,

            "online": online,

        }

    )
# ===========================================
# CHAT LIST PAGE
# ===========================================

@login_required
def chats(request):

    conversation_user_ids = set(

        Message.objects.filter(
            sender=request.user
        ).values_list(
            "receiver",
            flat=True
        )

    ) | set(

        Message.objects.filter(
            receiver=request.user
        ).values_list(
            "sender",
            flat=True
        )

    )

    conversation_list = []

    for uid in conversation_user_ids:

        person = User.objects.get(id=uid)

        last_msg = Message.objects.filter(

            sender__in=[request.user, person],

            receiver__in=[request.user, person]

        ).order_by("-created_at").first()

        if last_msg:

            if getattr(last_msg, "shared_post", None):

                preview = "📷 Shared a Post"

            else:

                is_reel, _ = _reel_share_preview(last_msg.message)

                preview = (
                    "🎬 Shared a Reel"
                    if is_reel
                    else last_msg.message
                )

            last_time = last_msg.created_at

        else:

            preview = "No messages yet"

            last_time = timezone.make_aware(
                timezone.datetime.min
            )

        conversation_list.append({

            "person": person,

            "last_message": preview,

            "time": last_time,

        })

    conversation_list.sort(

        key=lambda x: x["time"],

        reverse=True

    )

    return render(

        request,

        "chat/chat_list.html",

        {

            "conversation_list": conversation_list

        }

    )
from django.template.loader import render_to_string

@login_required
def chat_list_refresh(request):

    conversation_user_ids = set(

        Message.objects.filter(
            sender=request.user
        ).values_list(
            "receiver",
            flat=True
        )

    ) | set(

        Message.objects.filter(
            receiver=request.user
        ).values_list(
            "sender",
            flat=True
        )

    )

    conversation_list = []

    for uid in conversation_user_ids:

        person = User.objects.get(id=uid)

        last_msg = Message.objects.filter(

            sender__in=[request.user, person],

            receiver__in=[request.user, person]

        ).order_by("-created_at").first()

        unread = Message.objects.filter(
            sender=person,
            receiver=request.user,
            is_read=False
        ).count()

        if last_msg:

            if getattr(last_msg, "shared_post", None):

                preview = "📷 Shared a Post"

            else:

                is_reel, _ = _reel_share_preview(last_msg.message)

                preview = (
                    "🎬 Shared a Reel"
                    if is_reel
                    else last_msg.message
                )

        else:

            preview = ""

        conversation_list.append({

            "person": person,

            "last_message": preview,

            "time": last_msg.created_at if last_msg else timezone.now(),

            "unread": unread,

        })

    conversation_list.sort(
        key=lambda x: x["time"],
        reverse=True
    )

    html = render_to_string(

        "chat/chat_list_items.html",

        {

            "conversation_list": conversation_list

        },

        request=request

    )

    return JsonResponse({

        "html": html

    })
# ===========================================
# AJAX - GET MESSAGES
# ===========================================

@login_required
def get_messages(request, user_id):

    other_user = get_object_or_404(
        User,
        id=user_id
    )

    # Mark received messages as read
    Message.objects.filter(
        sender=other_user,
        receiver=request.user,
        is_read=False
    ).update(is_read=True)

    chat_messages = Message.objects.filter(
        sender__in=[request.user, other_user],
        receiver__in=[request.user, other_user]
    ).order_by("created_at")

    data = []

    for msg in chat_messages:

        is_reel, reel = _reel_share_preview(msg.message)

        data.append({

            "id": msg.id,

            "mine": msg.sender == request.user,

            "sender": msg.sender.username,

            "message": msg.message,

            "time": msg.created_at.strftime("%I:%M %p"),

            "is_read": msg.is_read,

            # reel
            "is_reel": is_reel,

            "reel_id": reel.id if reel else None,

            "reel_video": reel.video.url if reel else None,

            "reel_likes": reel.total_likes() if reel else 0,

            "reel_comments": reel.comments.count() if reel else 0,

            # post
            "is_post": msg.shared_post is not None,

            "post_id": msg.shared_post.id if msg.shared_post else None,

            "reply_to": {
                "user": msg.reply_to.sender.username,
                "message": msg.reply_to.message,
            } if msg.reply_to else None,

        })

    return JsonResponse({
        "messages": data
    })


    
# ===========================================
# TYPING STATUS
# ===========================================

@login_required
def typing_status(request):

    if request.method == "POST":

        status, created = TypingStatus.objects.get_or_create(

            user=request.user

        )

        status.is_typing = (

            request.POST.get("typing") == "true"

        )

        status.save()

        return JsonResponse({

            "success": True

        })

    return JsonResponse({

        "success": False

    })


# ===========================================
# CHECK OTHER USER TYPING
# ===========================================

@login_required
def check_typing(request, user_id):

    other_user = get_object_or_404(

        User,

        id=user_id

    )

    status = TypingStatus.objects.filter(

        user=other_user

    ).first()

    return JsonResponse({

        "typing": status.is_typing if status else False

    })
@login_required
def delete_message(request, message_id):

    msg = get_object_or_404(Message, id=message_id)

    # Sender mattum thaan delete panna mudiyum
    if msg.sender != request.user:
        return JsonResponse({"success": False, "error": "Not allowed"}, status=403)

    if request.method == "POST":
        msg.delete()
        return JsonResponse({"success": True})

    return JsonResponse({"success": False}, status=400)