from django.db import models
from django.contrib.auth.models import User


class Post(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="posts"
    )

    caption = models.TextField(
        max_length=1000
    )

    image = models.ImageField(
        upload_to="posts/",
        blank=True,
        null=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    likes = models.ManyToManyField(
        User,
        blank=True,
        related_name="liked_posts"
    )

    class Meta:
        ordering = ["-created_at"]

    def total_likes(self):
        return self.likes.count()

    def __str__(self):
        return f"{self.user.username} - {self.caption[:30]}"