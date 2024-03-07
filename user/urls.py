from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .account.urls import account_routes
from .auth.urls import auth_api_routes

app_name = "user"

router = DefaultRouter()


urlpatterns = [
    path("auth/", include(auth_api_routes)),
    path("account/", include(account_routes)),
]
