from django.db import models
from django.contrib.auth.models import User
from posts.models import Post


class Message(models.Model):

    sender = models.ForeignKey(
        User,
        related_name="sent_messages",
        on_delete=models.CASCADE
    )

    receiver = models.ForeignKey(
        User,
        related_name="received_messages",
        on_delete=models.CASCADE
    )

    message = models.TextField()

    # Shared Post
    shared_post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="shared_messages"
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    is_read = models.BooleanField(
        default=False
    )
    reply_to = models.ForeignKey(
    "self",
    null=True,
    blank=True,
    on_delete=models.SET_NULL,
    related_name="replies"
)

    class Meta:
        ordering = ["created_at"]

    def __str__(self):
        return f"{self.sender.username} -> {self.receiver.username}"


class TypingStatus(models.Model):

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE
    )

    is_typing = models.BooleanField(
        default=False
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return self.user.username


class Call(models.Model):

    CALL_TYPE_CHOICES = [
        ("video", "Video"),
        ("audio", "Audio"),
    ]

    STATUS_CHOICES = [
        ("ringing", "Ringing"),
        ("accepted", "Accepted"),
        ("rejected", "Rejected"),
        ("missed", "Missed"),
        ("ended", "Ended"),
    ]

    caller = models.ForeignKey(
        User,
        related_name="calls_made",
        on_delete=models.CASCADE
    )

    receiver = models.ForeignKey(
        User,
        related_name="calls_received",
        on_delete=models.CASCADE
    )

    call_type = models.CharField(
        max_length=10,
        choices=CALL_TYPE_CHOICES,
        default="video"
    )

    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default="ringing"
    )

    # WebRTC signaling data
    offer = models.TextField(null=True, blank=True)
    answer = models.TextField(null=True, blank=True)

    caller_candidates = models.JSONField(default=list, blank=True)
    receiver_candidates = models.JSONField(default=list, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    ended_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.call_type} call: {self.caller.username} -> {self.receiver.username} ({self.status})"