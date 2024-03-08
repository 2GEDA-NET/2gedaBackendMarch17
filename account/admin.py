from django.contrib import admin

from . import models as m


@admin.register(m.UserProfileMedia)
class ProfileMediaAdmin(admin.ModelAdmin):
    list_display = ("media",)


@admin.register(m.UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
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


@admin.register(m.UserAddress)
class AddressAdmin(admin.ModelAdmin):
    list_display = ("country", "state", "city")
