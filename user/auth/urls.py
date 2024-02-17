from django.urls import include, path
from rest_framework.routers import DefaultRouter

from . import api

router = DefaultRouter()
router.register("", api.AuthenticationViewSet, basename="auth")

auth_api_routes = [
    path("", include(router.urls)),
    path("login/", api.UserLoginAPI.as_view()),
    path("register/", api.UserRegistrationAPI.as_view()),
]
