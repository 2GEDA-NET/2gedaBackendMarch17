from django.contrib.auth import get_user_model
from rest_framework import decorators, status, viewsets
from rest_framework.response import Response

from . import models as m
from . import serializers as s
from utils import renderers

User = get_user_model()


class UserProfileAPI(viewsets.GenericViewSet):
    """User Profile Api"""

    serializer_class = s.UserProfileSerializer

    def get_queryset(self):
        queryset = m.UserProfile.objects.filter(user=self.request.user)
        return queryset

    def get_serializer_class(self):
        if self.action == "update_profile":
            return s.UserProfileUpdateSerializer
        return s.UserProfileSerializer

    @decorators.action(methods=["GET"], detail=False, url_path="retrieve")
    def get_profile(self, request, *args, **kwargs):
        response = {}
        status_code = None
        user_profile = self.get_queryset()
        if user_profile.exists():
            profile = user_profile.first()
            response["message"] = "Success"
            response["status"] = True
            response["data"] = s.UserProfileSerializer(
                profile, context={"request": request}
            ).data
            status_code = status.HTTP_200_OK
        else:
            response["message"] = "Fail to fetch data."
            response["status"] = False
            status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return Response(response, status=status_code)

    @decorators.action(methods=["PUT", "PATCH"], detail=False, url_path="update")
    def update_profile(self, request, *args, **kwargs):
        data = request.data
        user_data = data.pop("user", None)
        address = data.pop("address", None)
        if user_data:
            User.objects.filter(pk=request.user.id).update(**user_data)
        if address:
            # print("ADDRESS: ", address)
            user_address = m.UserAddress.objects.filter(profile=request.user.profile)
            user_address.update(**address)
        profile = m.UserProfile.objects.filter(user=request.user)
        profile.update(**data)
        return Response(
            {
                "message": "Profile updated successfully!",
                "status": True,
                "data": s.UserProfileUpdateSerializer(
                    profile.first(), context={"request": request}
                ).data,
            },
            status=status.HTTP_200_OK,
        )


class UserProfileMediaAPI(
    renderers.CreateModelRenderer,
    renderers.DestroyModelRenderer,
    viewsets.GenericViewSet,
):
    serializer_class = s.UserProfileMediaSerializer
    queryset = m.UserProfileMedia.objects.all()
    lookup_url_kwarg = "media_id"


class UserProfileImageMediaAPI(
    renderers.ReadOnlyModelRenderer,
    renderers.DestroyModelRenderer,
    viewsets.GenericViewSet,
):
    serializer_class = s.UserProfileMediaSerializer
    lookup_url_kwarg = "image_id"

    def get_queryset(self):
        return m.UserProfileMedia.objects.filter(media_type="image")


class UserProfileFileMediaAPI(
    renderers.ReadOnlyModelRenderer,
    renderers.DestroyModelRenderer,
    viewsets.GenericViewSet,
):
    serializer_class = s.UserProfileMediaSerializer
    lookup_url_kwarg = "file_id"

    def get_queryset(self):
        return m.UserProfileMedia.objects.filter(media_type="file")


class UserProfileVoiceNoteMediaAPI(
    renderers.ReadOnlyModelRenderer,
    renderers.DestroyModelRenderer,
    viewsets.GenericViewSet,
):
    serializer_class = s.UserProfileMediaSerializer
    lookup_url_kwarg = "voice_note_id"

    def get_queryset(self):
        return m.UserProfileMedia.objects.filter(media_type="voice_note")


class UserProfileVideoMediaAPI(
    renderers.ReadOnlyModelRenderer,
    renderers.DestroyModelRenderer,
    viewsets.GenericViewSet,
):
    serializer_class = s.UserProfileMediaSerializer
    lookup_url_kwarg = "video_id"

    def get_queryset(self):
        return m.UserProfileMedia.objects.filter(media_type="video")
