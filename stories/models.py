from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta


class Story(models.Model):

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="stories"
    )

    image = models.ImageField(
        upload_to="stories/"
    )

    caption = models.CharField(
        max_length=200,
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    expires_at = models.DateTimeField(
        default=timezone.now
    )

    def save(self, *args, **kwargs):
        if not self.pk:
            self.expires_at = timezone.now() + timedelta(hours=24)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.user.username


class StorySeen(models.Model):

    story = models.ForeignKey(
        Story,
        on_delete=models.CASCADE,
        related_name="seen_users"
    )

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    seen_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        unique_together = ("story", "user")

    def __str__(self):
        return f"{self.user.username} viewed Story {self.story.id}"


class Highlight(models.Model):

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    title = models.CharField(
        max_length=50
    )

    cover = models.ImageField(
        upload_to="highlight_covers/"
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.title


class HighlightStory(models.Model):

    highlight = models.ForeignKey(
        Highlight,
        on_delete=models.CASCADE,
        related_name="highlight_stories"
    )

    story = models.ForeignKey(
        Story,
        on_delete=models.CASCADE
    )

    def __str__(self):
        return f"{self.highlight.title} - Story {self.story.id}"


class StoryReaction(models.Model):

    EMOJIS = [
        ("❤️", "❤️"),
        ("😂", "😂"),
        ("😍", "😍"),
        ("🔥", "🔥"),
        ("😮", "😮"),
    ]

    story = models.ForeignKey(
        Story,
        on_delete=models.CASCADE,
        related_name="reactions"
    )

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    emoji = models.CharField(
        max_length=5,
        choices=EMOJIS
    )

    reacted_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        unique_together = ("story", "user")

    def __str__(self):
        return f"{self.user.username} reacted {self.emoji}"