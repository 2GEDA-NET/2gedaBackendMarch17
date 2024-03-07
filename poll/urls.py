from django.urls import include, path
from rest_framework.routers import DefaultRouter

from . import api

app_name = "poll"

router = DefaultRouter()
router.register("user", api.UserPollAPI, basename="user_poll")
router.register("", api.PollsAPI, basename="poll")


urlpatterns = [path("", include(router.urls))]
