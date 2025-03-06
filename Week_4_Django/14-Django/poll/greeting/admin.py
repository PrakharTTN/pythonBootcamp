from django.contrib import admin
from .models import Vote, Poll

# Register your models here.


@admin.register(Poll)
class PollAdmin(admin.ModelAdmin):
    list_display = ("question_text", "created_at", "is_active")


@admin.register(Vote)
class VoteAdmin(admin.ModelAdmin):
    list_display = ("poll", "user", "created_at")
