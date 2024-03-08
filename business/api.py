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


class BusinessOwnerProfileAPI(renderers.CreateModelRenderer, viewsets.GenericViewSet):
    queryset = m.BusinessOwnerProfile.objects.all()
    serializer_class = s.BusinessOwnerProfileSerializer


# from django.shortcuts import render
# from rest_framework import viewsets
# from .models import BusinessDirectory, Address, PhoneNumber
# from rest_framework.views import APIView
# from .serializers import *
# from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
# from rest_framework.authentication import *
# from rest_framework import status
# from rest_framework.response import Response


# class AddressViewSet(viewsets.ModelViewSet):
#     permission_classes = (IsAuthenticated,)
#     authentication_classes = (TokenAuthentication,)
#     queryset = Address.objects.all()
#     serializer_class = BusinessAddressSerializer


# class PhoneNumberViewSet(viewsets.ModelViewSet):
#     permission_classes = (IsAuthenticated,)
#     authentication_classes = (TokenAuthentication,)
#     queryset = PhoneNumber.objects.all()
#     serializer_class = PhoneNumberSerializer


# class BusinessDirectoryViewSet(viewsets.ModelViewSet):
#     permission_classes = (IsAuthenticated,)
#     authentication_classes = (TokenAuthentication,)
#     queryset = BusinessDirectory.objects.all()
#     serializer_class = BusinessDirectorySerializer


# class BusinessClaimView(APIView):
#     def post(self, request, format=None):
#         serializer = BusinessClaimSerializer(data=request.data)
#         if serializer.is_valid():
#             business_id = serializer.validated_data["business_id"]
#             user_id = serializer.validated_data["user_id"]

#             # Create or retrieve the BusinessOwnerProfile
#             user_profile, created = BusinessOwnerProfile.objects.get_or_create(
#                 user_id=user_id,
#                 defaults={
#                     "first_name": serializer.validated_data[
#                         "business_owner_first_name"
#                     ],
#                     "last_name": serializer.validated_data["business_owner_last_name"],
#                     "phone_number": serializer.validated_data[
#                         "business_owner_phone_number"
#                     ],
#                     "email": serializer.validated_data["business_owner_email"],
#                 },
#             )

#             # Update the claimed_by field in the BusinessDirectory
#             business = BusinessDirectory.objects.get(id=business_id)
#             business.claimed_by = user_profile
#             business.name = serializer.validated_data["business_name"]
#             business.about = serializer.validated_data["business_description"]
#             business.email = serializer.validated_data["business_email"]
#             business.website = serializer.validated_data.get("business_website", "")

#             # Save the updated business details
#             business.save()

#             # Handle business documents (e.g., license, tax ID)
#             # You can add logic here to create BusinessDocument instances for each document type

#             return Response(
#                 {"message": "Business claimed successfully."}, status=status.HTTP_200_OK
#             )

#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
