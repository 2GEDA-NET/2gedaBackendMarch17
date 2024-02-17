from django.urls import include, path
from rest_framework.routers import DefaultRouter

# from . import api
from .auth.urls import auth_api_routes
from .account.urls import account_routes

router = DefaultRouter()


urlpatterns = [
    path("", include(auth_api_routes)),
    path("", include(account_routes)),
]
