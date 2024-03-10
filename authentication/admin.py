from django.contrib import admin

from .models import OneTimePassword, User


@admin.register(User)
class UsersAdmin(admin.ModelAdmin):
    list_display = (
        "email",
        "username",
        "first_name",
        "last_name",
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