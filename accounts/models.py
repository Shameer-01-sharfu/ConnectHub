from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE
    )

    profile_picture = models.ImageField(
        upload_to="profile_pictures/",
        default="default_profile.png"
    )

    cover_picture = models.ImageField(
        upload_to="cover_pictures/",
        default="default_cover.jpg"
    )

    bio = models.TextField(
        blank=True,
        max_length=300
    )

    location = models.CharField(
        max_length=100,
        blank=True
    )

    website = models.URLField(
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.user.username