from django.contrib import admin
from import_export.admin import ImportExportModelAdmin

from .account import models as acc
from .auth.models import OneTimePassword, User


@admin.register(User)
class UsersAdmin(ImportExportModelAdmin):
    list_display = (
        "username",
        "first_name",
        "last_name",
        "email",
        "phone_number",
        "is_business",
        "is_personal",
        "is_admin",
        "is_verified",
    )
    readonly_fields = (
        "email",
        "password",
        "username",
        "phone_number",
        "last_login",
        "date_joined",
    )
    search_fields = ("email", "phone_number")
    list_editable = [
        "is_business",
        "is_personal",
        "is_admin",
    ]
    list_filter = ()

    fieldsets = (
        (
            "Authentication",
            {"fields": ("email", "username", "phone_number")},
        ),
        (
            "Personal Information",
            {"fields": ("first_name", "last_name", "is_personal", "is_business")},
        ),
        (
            "Permissions",
            {"fields": ("is_active", "is_verified", "is_staff", "is_superuser")},
        ),
        ("Important dates", {"fields": ("last_login", "date_joined")}),
    )

    add_fieldsets = (
        (None, {"fields": ("email", "phone_number", "password1", "password2")}),
        ("Permissions", {"fields": ("is_verified", "is_staff", "is_superuser")}),
    )


@admin.register(OneTimePassword)
class OneTimePasswordAdmin(admin.ModelAdmin):
    list_display = ["user", "otp", "verification_type", "created_at"]


@admin.register(acc.ProfileMedia)
class ProfileMediaAdmin(ImportExportModelAdmin):
    list_display = ("media",)


@admin.register(acc.Sticker)
class StickerAdmin(admin.ModelAdmin):
    list_display = ["sticker", "sticked", "sticked_on"]


@admin.register(acc.UserProfile)
class UserProfileAdmin(ImportExportModelAdmin):
    list_display = (
        "user",
        "occupation",
        "date_of_birth",
        "gender",
    )
    list_filter = ("gender",)
    search_fields = [
        "user",
    ]


@admin.register(acc.ReportedUser)
class ReportedUserAdmin(ImportExportModelAdmin):
    list_display = ("user", "is_banned", "is_disabled")
    list_editable = [
        "is_banned",
        "is_disabled",
    ]


@admin.register(acc.UserAddress)
class AddressAdmin(ImportExportModelAdmin):
    list_display = ("country", "state", "city")


@admin.register(acc.Verification)
class VerificationAdmin(ImportExportModelAdmin):
    list_display = ("profile", "legal_name", "work")


@admin.register(acc.Notification)
class NotificationAdmin(ImportExportModelAdmin):
    list_display = ("recipient", "sender", "message", "timestamp")


@admin.register(acc.Device)
class DeviceAdmin(ImportExportModelAdmin):
    list_display = ("name", "category", "input")


admin.site.site_header = "2geda Administration Dashboard"
