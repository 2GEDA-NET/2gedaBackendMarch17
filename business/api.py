from rest_framework import decorators, status, viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from utils import renderers

from . import models as m
from . import serializers as s
from .permissions import IsBusinessAccount


class BusinessAccountAPI(renderers.ListCreateModelRenderer, viewsets.GenericViewSet):

    def get_queryset(self):
        return m.BusinessAccount.objects.filter(profile=self.request.user.profile)

    def get_serializer_class(self):
        if self.action == "verify":
            return s.BusinessVerificationSerializer
        return s.BusinessAccountSerializer

    def perform_create(self, serializer):
        serializer.save(profile=self.request.user.profile)

    def create(self, request, *args, **kwargs):
        # Example of `availability` request data: Must time obj serializable ["10:12:53"]
        """
        ```
        "availability": {
            "monday": {
                "open_from": "10:12:53",
                "close_at": "10:12:55"
            },
            "tuesday": {
                "open_from": "06:00:00",
                "close_at": "10:14:44"
            },
            "wednesday": {
                "open_from": "10:14:50",
                "close_at": "10:14:50"
            },
            "thursday": {
                "open_from": "10:14:55",
                "close_at": "10:14:55"
            },
            "friday": {
                "open_from": "10:15:00",
                "close_at": "10:15:01"
            },
            "saturday": {
                "open_from": "10:15:06",
                "close_at": "10:15:07"
            },
            "sunday": {
                "open_from": "10:15:12",
                "close_at": "10:15:13"
            }
        }
        ```
        **category** --> ```personal``` | ```company```
        """
        data = super().create(request, *args, **kwargs).data
        data["message"] = "Business account created successfully!"
        return Response(data, status=status.HTTP_201_CREATED)

    @decorators.action(methods=["POST"], detail=False, url_path="verify")
    def verify(self, request, *args, **kwargs):
        serializer = self.get_serializer_class()(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            {"message": "Success", "status": True, "data": serializer.data},
            status=status.HTTP_201_CREATED,
        )
