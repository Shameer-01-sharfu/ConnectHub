from django.contrib import admin
from .models import Post, SavedPost


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user",
        "caption",
        "created_at",
    )

    search_fields = (
        "user__username",
        "caption",
    )

    list_filter = (
        "created_at",
    )


@admin.register(SavedPost)
class SavedPostAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user",
        "post",
        "saved_at",
    )

    search_fields = (
        "user__username",
        "post__caption",
    )

    list_filter = (
        "saved_at",
    )