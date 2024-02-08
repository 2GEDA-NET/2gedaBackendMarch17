from django.urls import include, path
from rest_framework.routers import DefaultRouter

from . import views as v

router = DefaultRouter()
router.register("", v.ArtistAPI, basename="stereo")

urlpatterns = [path("", include(router.urls))]
