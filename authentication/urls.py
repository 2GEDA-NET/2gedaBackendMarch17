from django.urls import include, path
from rest_framework.routers import DefaultRouter

from . import api

app_name = "authentication"

router = DefaultRouter()
router.register("", api.AuthenticationViewSet, basename="auth")


urlpatterns = [
    path("", include(router.urls)),
    path("login/", api.UserLoginAPI.as_view()),
    path("register/", api.UserRegistrationAPI.as_view()),
]
