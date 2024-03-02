from django.urls import include, path
from rest_framework.routers import DefaultRouter

from . import api

router = DefaultRouter()
router.register("profile", api.UserProfileAPI, basename="profile")

account_routes = [path("", include(router.urls))]
