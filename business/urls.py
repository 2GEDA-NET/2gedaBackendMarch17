from django.urls import include, path
from rest_framework.routers import DefaultRouter

from . import api

app_name = "business"

router = DefaultRouter()
router.register("", api.BusinessAccountAPI, basename="business")
router.register("categories", api.BusinessCategoryAPI, basename="categories")
router.register("owner/verify", api.BusinessOwnerProfileAPI, basename="owner")

urlpatterns = [
    path("", include(router.urls)),
]
