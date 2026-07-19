from django.contrib import admin
from .models import Story, StorySeen, Highlight, HighlightStory


@admin.register(Story)
class StoryAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "user",
        "created_at",
        "expires_at",
    )

    search_fields = (
        "user__username",
    )

    list_filter = (
        "created_at",
    )


@admin.register(StorySeen)
class StorySeenAdmin(admin.ModelAdmin):

    list_display = (
        "story",
        "user",
        "seen_at",
    )


@admin.register(Highlight)
class HighlightAdmin(admin.ModelAdmin):

    list_display = (
        "title",
        "user",
        "created_at",
    )


@admin.register(HighlightStory)
class HighlightStoryAdmin(admin.ModelAdmin):

    list_display = (
        "highlight",
        "story",
    )