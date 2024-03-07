from django.contrib import admin

from . import models as m


@admin.register(m.Poll)
class PollAdmin(admin.ModelAdmin):
    list_display = ["question", "is_closed", "close_time"]


@admin.register(m.PollOption)
class PollOptionAdmin(admin.ModelAdmin):
    list_display = ["content"]
