from django.contrib import admin

from . import models as m


@admin.register(m.Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ("user", "text_content", "is_business_post", "is_personal_post")


@admin.register(m.SharePost)
class SharePostAdmin(admin.ModelAdmin):
    list_display = ("user", "caption", "shared_post", "created_at")


@admin.register(m.Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ("user", "post", "text_content", "created_at")


@admin.register(m.Reply)
class ReplyAdmin(admin.ModelAdmin):
    list_display = ("user", "comment", "text_content", "created_at")


@admin.register(m.SavedPost)
class SavedPostAdmin(admin.ModelAdmin):
    list_display = ("user", "post", "created_at")
