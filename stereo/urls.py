from django.urls import include, path
from rest_framework.routers import DefaultRouter

from . import api

router = DefaultRouter()
router.register("album", api.AlbumAPI, basename="album")
router.register("artists", api.ArtistAPI, basename="artist")
router.register("library", api.SongLibraryAPI, basename="library")
router.register("songs", api.SongAPI, basename="song")

urlpatterns = [path("", include(router.urls))]
