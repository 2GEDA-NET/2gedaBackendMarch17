from django.urls import include, path
from rest_framework.routers import DefaultRouter

from . import api

app_name = "notifications"

router = DefaultRouter()
router.register("", api.NotificationAPI, basename="notification")

urlpatterns = [path("", include(router.urls))]
