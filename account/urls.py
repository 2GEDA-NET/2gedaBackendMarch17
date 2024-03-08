from django.urls import include, path
from rest_framework.routers import DefaultRouter

from . import api

app_name = "account"

router = DefaultRouter()
router.register("profile", api.UserProfileAPI, basename="profile")
router.register("profile/media", api.UserProfileMediaAPI, basename="media")
router.register("profile/media/images", api.UserProfileImageMediaAPI, basename="image")
router.register("profile/media/videos", api.UserProfileVideoMediaAPI, basename="video")
router.register("profile/media/files", api.UserProfileFileMediaAPI, basename="file")
router.register(
    "profile/media/voice-notes", api.UserProfileVoiceNoteMediaAPI, basename="voice_note"
)

urlpatterns = [path("", include(router.urls))]
