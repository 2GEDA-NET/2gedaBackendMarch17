from rest_framework import status, viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from utils import renderers

from . import models as m
from . import serializers as s
from .permissions import IsBusinessOwnerProfile


class BusinessAccountAPI(renderers.ListCreateModelRenderer, viewsets.GenericViewSet):

    serializer_class = s.BusinessAccountSerializer

    def get_queryset(self):
        return m.BusinessAccount.objects.filter(user=self.request.user)

    def get_permissions(self):
        if self.action == "create":
            permissions = [AllowAny]
        else:
            permissions = [IsAuthenticated]
        return [permission() for permission in permissions]

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
        """
        data = super().create(request, *args, **kwargs).data
        data["message"] = "Business account created successfully!"
        return Response(data, status=status.HTTP_201_CREATED)


class BusinessCategoryAPI(
    renderers.ListRetrieveCreateModelRenderer, viewsets.GenericViewSet
):
    queryset = m.BusinessCategory.objects.all()
    serializer_class = s.BusinessCategorySerializer
    lookup_url_kwarg = "category_id"


class BusinessOwnerProfileAPI(renderers.CreateModelRenderer, viewsets.GenericViewSet):
    queryset = m.BusinessOwnerProfile.objects.all()
    serializer_class = s.BusinessOwnerProfileSerializer
