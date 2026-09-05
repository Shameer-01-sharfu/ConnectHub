from django.contrib import admin
from .models import Reel, ReelComment


@admin.register(Reel)
class ReelAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "user",
        "created_at"
    )


@admin.register(ReelComment)
class ReelCommentAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "user",
        "reel",
        "created_at"
    )