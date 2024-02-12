from django.urls import include, path
from rest_framework.routers import DefaultRouter

from . import views as v

router = DefaultRouter()
router.register("artists", v.ArtistAPI, basename="artist")
router.register("songs", v.SongAPI, basename="song")
router.register("library", v.SongLibraryAPI, basename="library")

urlpatterns = [path("", include(router.urls))]
