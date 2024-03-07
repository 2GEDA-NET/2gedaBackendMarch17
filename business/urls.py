from django.urls import include, path
from rest_framework.routers import DefaultRouter

from . import api

app_name = "business"

router = DefaultRouter()
router.register("", api.BusinessAccountAPI, basename="business")
router.register("categories", api.BusinessCategoryAPI, basename="categories")
router.register(
    "business-owner", api.BusinessOwnerProfileAPI, basename="business_owner"
)

urlpatterns = [
    # path("", api.BusinessAccountAPI.as_view(), name="business"),
    # path("categories/", api.BusinessCategoryAPI.as_view(), name="categories"),
    path("", include(router.urls)),
]
