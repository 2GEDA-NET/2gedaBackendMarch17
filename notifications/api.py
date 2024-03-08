from rest_framework import decorators, status, viewsets
from rest_framework.response import Response

from utils import renderers

from . import models as m
from . import serializers as s


class NotificationAPI(renderers.ReadOnlyModelRenderer, viewsets.GenericViewSet):
    serializer_class = s.NotificationSerializer
    lookup_url_kwarg = "notification_id"

    def get_queryset(self):
        profile = self.request.user.profile
        if self.action == "read":
            return m.Notification.objects.filter(profile=profile, is_seen=True)
        elif self.action == "unread":
            return m.Notification.objects.filter(profile=profile, is_seen=False)
        return m.Notification.objects.filter(profile=profile)

    def retrieve(self, request, *args, **kwargs):
        notification = self.get_object()
        notification.is_seen = True
        notification.save()
        return super().retrieve(request, *args, **kwargs)

    @decorators.action(methods=["GET"], detail=False, url_path="read")
    def read(self, request, *args, **kwargs):
        notifications = self.get_queryset()
        data = self.serializer_class(notifications, many=True).data
        return Response(
            {"message": "Success", "status": True, "data": data},
            status=status.HTTP_200_OK,
        )

    @decorators.action(methods=["GET"], detail=False, url_path="unread")
    def unread(self, request, *args, **kwargs):
        notifications = self.get_queryset()
        data = self.serializer_class(notifications, many=True).data
        return Response(
            {"message": "Success", "status": True, "data": data},
            status=status.HTTP_200_OK,
        )
