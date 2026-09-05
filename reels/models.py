from django.db import models
from django.contrib.auth.models import User
from django.conf import settings


def reel_video_storage():
    """
    Reel videos must upload to Cloudinary as resource_type="video".
    The project's default Cloudinary storage (STORAGES["default"]) is
    configured for images, so uploading an .mp4 through it fails with
    a Cloudinary API error (surfaces as a 500 on the reel upload view).
    Falls back to the local filesystem when Cloudinary isn't configured
    (e.g. local development without CLOUDINARY_* env vars set).
    """
    if getattr(settings, "USE_CLOUDINARY", False):
        from cloudinary_storage.storage import VideoMediaCloudinaryStorage
        return VideoMediaCloudinaryStorage()
    from django.core.files.storage import default_storage
    return default_storage


class Reel(models.Model):

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="reels"
    )

    caption = models.TextField(
        blank=True,
        max_length=500
    )

    video = models.FileField(
        upload_to="reels/",
        storage=reel_video_storage
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    likes = models.ManyToManyField(
        User,
        blank=True,
        related_name="liked_reels"
    )

    saved_by = models.ManyToManyField(
        User,
        blank=True,
        related_name="saved_reels"
    )

    views = models.ManyToManyField(
    User,
    related_name="viewed_reels",
    blank=True
)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.user.username} Reel"

    def total_likes(self):
        return self.likes.count()
    
class ReelComment(models.Model):

    reel = models.ForeignKey(
        Reel,
        on_delete=models.CASCADE,
        related_name="comments"
    )

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    comment = models.TextField(
        max_length=300
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        ordering = ["created_at"]

    def __str__(self):
        return f"{self.user.username} - {self.comment[:25]}"
    
class ReelShare(models.Model):

    sender = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="reels_sent"
    )

    receiver = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="reels_received"
    )

    reel = models.ForeignKey(
        Reel,
        on_delete=models.CASCADE,
        related_name="shares"
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:

        ordering = ["-created_at"]

        unique_together = ("sender", "receiver", "reel")

    def __str__(self):

        return f"{self.sender} → {self.receiver}"