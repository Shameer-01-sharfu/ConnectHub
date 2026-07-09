from django.contrib import admin
from .models import Post


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = (
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