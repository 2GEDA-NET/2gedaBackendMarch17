from django.contrib import admin

from . import models as m


@admin.register(m.BusinessAccount)
class BusinessAccountAdmin(admin.ModelAdmin):
    list_display = ["user", "business_name", "business_email", "is_verified"]


@admin.register(m.BusinessCategory)
class BusinessCategory(admin.ModelAdmin):
    list_display = ["name"]


@admin.register(m.BusinessDayAvailability)
class BusinessDayAvailabilityAdmin(admin.ModelAdmin):
    list_display = ["business"]


@admin.register(m.BusinessTimeAvailability)
class BusinessTimeAvailabilityAdmin(admin.ModelAdmin):
    list_display = ["open_from", "close_at"]
