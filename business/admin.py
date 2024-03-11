from django.contrib import admin

from . import models as m


@admin.register(m.BusinessAccount)
class BusinessAccountAdmin(admin.ModelAdmin):
    list_display = ["user", "business_name", "is_verified"]


@admin.register(m.BusinessDayAvailability)
class BusinessDayAvailabilityAdmin(admin.ModelAdmin):
    list_display = [
        "business",
        "monday",
        "tuesday",
        "wednesday",
        "thursday",
        "friday",
        "saturday",
        "sunday",
    ]


@admin.register(m.BusinessTimeAvailability)
class BusinessTimeAvailabilityAdmin(admin.ModelAdmin):
    list_display = ["open_from", "close_at"]
