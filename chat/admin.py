from django.contrib import admin
from .models import Message, TypingStatus, Call


@admin.register(Call)
class CallAdmin(admin.ModelAdmin):
    list_display = ("id", "caller", "receiver", "call_type", "status", "created_at", "ended_at")
    list_filter = ("call_type", "status")
    search_fields = ("caller__username", "receiver__username")
