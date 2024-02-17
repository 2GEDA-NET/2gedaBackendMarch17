import datetime
from ctypes import pointer

from django.contrib.auth import get_user_model, login
from django.db.models import Q
from django.views.decorators.csrf import csrf_exempt
from rest_framework import decorators, generics, status, views, viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.decorators import (
    api_view,
    authentication_classes,
    permission_classes,
)
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from business.models import BusinessDirectory
from chat.models import Conversation, Participant
from feed.models import CommentMedia, PostMedia
from user.auth.serializers import UserSerializer

from . import models as m
from . import serializers as s

User = get_user_model()


class BusinessAccountLoginView(views.APIView):
    def post(self, request):
        serializer = s.BusinessAccountLoginSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data["business_name"]
            password = serializer.validated_data["business_password"]
            user = s.BusinessAccountAuthBackend().authenticate(
                request, username=username, password=password
            )  # Use authenticate method
            if user is not None:
                login(request, user)
                token, created = Token.objects.get_or_create(user=user)
                return Response({"token": token.key}, status=status.HTTP_200_OK)
        return Response(
            {"detail": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED
        )


class ManagedBusinessAccountsView(generics.ListAPIView):
    serializer_class = s.BusinessAccountSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return s.BusinessAccount.objects.filter(profile__user=user)


# class BusinessAccountChangePasswordView(generics.UpdateAPIView):
#     serializer_class = s.BusinessAccountChangePasswordSerializer
#     permission_classes = [IsAuthenticated]

#     def get_object(self):
#         return self.request.user

#     def update(self, request, *args, **kwargs):
#         serializer = self.get_serializer(
#             data=request.data, context={"request": request}
#         )
#         if serializer.is_valid():
#             user = self.get_object()
#             new_password = serializer.validated_data["new_password"]
#             user.businessaccount.business_password = new_password
#             user.businessaccount.save()
#             return Response(
#                 {"detail": "Password has been changed successfully."},
#                 status=status.HTTP_200_OK,
#             )
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    # authentication_classes = (TokenAuthentication,)
    queryset = User.objects.all()
    # serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        location_data = request.data.get("location")
        if location_data:
            # Assuming location_data is a dictionary with 'latitude' and 'longitude' keys
            latitude = location_data.get("latitude")
            longitude = location_data.get("longitude")

            # Create or update user location
            user = self.perform_create(serializer)
            # Create a Point object from coordinates
            user.location = pointer(longitude, latitude)
            user.save()

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )


# End of User details APIs


# Sticking APIs
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def stick_user(request, user_id):
    user = request.user.userprofile
    try:
        target_user = m.UserProfile.objects.get(pk=user_id)
    except m.UserProfile.DoesNotExist:
        return Response({"message": "User not found"}, status=status.HTTP_404_NOT_FOUND)

    if user != target_user:
        if user.sticking.filter(pk=user_id).exists():
            user.sticking.remove(target_user)
            # If unsticking, remove the corresponding Participant record
            Participant.objects.filter(user=user.user, sticking_to=target_user).delete()
            # Send an unstick notification
            send_notification(
                target_user.user, f"You were unsticked by {user.user.username}"
            )
            return Response({"message": f"You unsticked {target_user.user.username}"})
        else:
            user.sticking.add(target_user)
            # If sticking, create a Participant record
            Participant.objects.create(user=user.user, sticking_to=target_user)
            # Send a stick notification
            send_notification(
                target_user.user, f"You were sticked by {user.user.username}"
            )
            return Response({"message": f"You sticked {target_user.user.username}"})

    return Response(
        {"message": "You cannot stick/unstick yourself"},
        status=status.HTTP_400_BAD_REQUEST,
    )


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def list_stickers(request, user_id):
    try:
        user_profile = m.UserProfile.objects.get(pk=user_id)
    except m.UserProfile.DoesNotExist:
        return Response({"message": "User not found"}, status=status.HTTP_404_NOT_FOUND)

    stickers = user_profile.stickers.all()
    serializer = s.UserListSerializer(stickers, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(["PUT"])
@permission_classes([IsAuthenticated])
def update_user_profile(request):
    user = request.user

    if request.method == "PUT":
        serializer = s.UserProfileUpdateSerializer(instance=user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "User profile updated successfully"})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def list_sticking(request, user_id):
    try:
        user_profile = m.UserProfile.objects.get(pk=user_id)
    except m.UserProfile.DoesNotExist:
        return Response({"message": "User not found"}, status=status.HTTP_404_NOT_FOUND)

    sticking = user_profile.sticking.all()
    serializer = s.UserListSerializer(sticking, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def my_sticking(request):
    user = request.user
    try:
        user_profile = m.UserProfile.objects.get(user=user)
        sticking = user_profile.sticking.all()
        sticking_data = [
            {
                "username": profile.user.username,
                "first_name": profile.user.first_name,
                "last_name": profile.user.last_name,
                "sticking_count": profile.sticking.count(),
                "sticker_count": profile.stickers.count(),
            }
            for profile in sticking
        ]
        return Response(sticking_data, status=status.HTTP_200_OK)
    except m.UserProfile.DoesNotExist:
        return Response(
            {"message": "User profile not found"}, status=status.HTTP_404_NOT_FOUND
        )


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def my_stickers(request):
    user = request.user
    try:
        user_profile = m.UserProfile.objects.get(user=user)
        stickers = user_profile.stickers.all()
        sticker_data = [
            {
                "username": profile.user.username,
                "first_name": profile.user.first_name,
                "last_name": profile.user.last_name,
                "sticking_count": profile.sticking.count(),
                "sticker_count": profile.stickers.count(),
            }
            for profile in stickers
        ]
        return Response(sticker_data, status=status.HTTP_200_OK)
    except m.UserProfile.DoesNotExist:
        return Response(
            {"message": "User profile not found"}, status=status.HTTP_404_NOT_FOUND
        )


# End of sticking APIs


class UserAPIView(generics.RetrieveAPIView):
    """
    Get user details
    """

    queryset = User.objects.all()
    serializer_class = UserSerializer
    # permission_classes = (IsAuthenticated,)

    def get_object(self):
        return self.request.user


# Report Users API


@api_view(["POST"])
@csrf_exempt
@permission_classes([AllowAny])
def report_user(request):
    if request.method == "POST":
        serializer = s.ReportUserSerializer(
            data=request.data, context={"request": request}
        )

        if serializer.is_valid():
            report = serializer.save()
            response_data = serializer.data
            return Response(response_data, status=status.HTTP_201_CREATED)
        else:
            return Response(
                {"error": "Report not successful"}, status=status.HTTP_400_BAD_REQUEST
            )


class ReportUserViewSet(generics.RetrieveAPIView):
    # permission_classes = (IsAuthenticated,)
    # authentication_classes = (TokenAuthentication,)
    queryset = m.ReportedUser.objects.all()
    serializer_class = s.ReportedUserSerializer
    lookup_field = "user_id"


# End of report users


class UserProfileViewSet(viewsets.ModelViewSet):
    # permission_classes = [IsAuthenticated]
    # authentication_classes = [TokenAuthentication]
    queryset = m.UserProfile.objects.all()
    serializer_class = s.UserProfileSerializer

    def get_object(self):
        return m.UserProfile.objects.get(user=self.request.user)

    def perform_update(self, serializer):
        user_profile = self.get_object()

        print("Received Data:")
        print(self.request.data)

        # Update the first name and last name fields
        user_profile.user.first_name = self.request.data.get("user")["first_name"]
        user_profile.user.last_name = self.request.data.get("user")["last_name"]
        date_of_birth = self.request.data.get("date_of_birth")
        user_profile.work = self.request.data.get("work")
        user_profile.gender = self.request.data.get("identity")
        user_profile.religion = self.request.data.get("religion")
        user_profile.custom_gender = self.request.data.get("custom_gender")
        profile_image_data = self.request.FILES["profile_image"]
        cover_image_data = self.request.FILES["cover_image"]

        print(cover_image_data)
        print(profile_image_data)

        if user_profile.gender == 1 or user_profile.gender == "Male":
            user_profile.gender = "Male"
        elif user_profile.gender == 2 or user_profile.gender == "Female":
            user_profile.gender = "Female"
        else:
            user_profile.gender = "Rather not say"

        if user_profile.religion == 1 or user_profile.religion == "Christain":
            user_profile.religion = "Christain"
        elif user_profile.religion == 2 or user_profile.religion == "Muslim":
            user_profile.religion = "Muslim"
        else:
            user_profile.religion = "Indegineous"

        if profile_image_data:
            # Assuming the field name in the serializer is 'profile_image'
            # You may need to adjust this based on your serializer
            user_profile.media.media = profile_image_data
            # Save the uploaded profile image

        if cover_image_data:
            # Assuming the field name in the serializer is 'cover_image'
            # You may need to adjust this based on your serializer
            user_profile.cover_image.media = cover_image_data
            # Save the uploaded cover image

        # Print the data for debugging
        print("Received Data:")
        print(f"first_name: {user_profile.user.first_name}")
        print(f"last_name: {user_profile.user.last_name}")
        print(f"work: {user_profile.work}")
        print(f"gender: {user_profile.gender}")
        print(f"custom_gender: {user_profile.custom_gender}")
        print(f"custom_gender: {user_profile.religion}")
        print(f"date_of_birth: {date_of_birth}")
        print(f"profile_image: {user_profile.media}")
        print(f"cover_image: {user_profile.cover_image}")

        # Check if date_of_birth is not empty before parsing it
        if date_of_birth:
            try:
                formatted_date = datetime.datetime.strptime(
                    date_of_birth, "%Y-%m-%d"
                ).date()
                user_profile.date_of_birth = formatted_date
                print(f"Parsed Date: {formatted_date}")
            except ValueError:
                return Response(
                    {"error": "Invalid date format. Please use YYYY-MM-DD."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

        # Save the user_profile object
        user_profile.save()
        user_profile.user.save()
        user_profile.media.save()
        print("Profile Saved")

        return Response({"message": "Profile updated successfully"})


# Business APIs
class BusinessCategoryViewSet(viewsets.ModelViewSet):
    # permission_classes = (IsAuthenticated,)
    # authentication_classes = (TokenAuthentication,)
    queryset = m.BusinessCategory.objects.all()
    serializer_class = s.BusinessCategorySerializer


@api_view(["POST"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def create_business_profile(request):
    if request.method == "POST":
        # Automatically associate the user's profile with the request data
        request.data["profile"] = request.user.userprofile.pk

        serializer = s.BusinessAccountSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()

            # Send a notification for profile creation
            send_notification(request.user, "Your business profile has been created.")

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["PUT"])
def update_business_profile(request, pk):
    try:
        business_profile = s.BusinessAccountSerializer.objects.get(pk=pk)
    except s.BusinessAccountSerializer.DoesNotExist:
        return Response(
            {"detail": "BusinessProfile not found"}, status=status.HTTP_404_NOT_FOUND
        )

    if request.method == "PUT":
        serializer = s.BusinessAccountSerializer(business_profile, data=request.data)
        if serializer.is_valid():
            serializer.save()

            # Send a notification for profile update
            send_notification(request.user, "Your business profile has been updated.")

            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BusinessAvailabilityListCreateView(generics.ListCreateAPIView):
    # authentication_classes = (TokenAuthentication,)
    permission_classes = [IsAuthenticated]
    queryset = m.BusinessAvailability.objects.all()
    serializer_class = s.BusinessAvailabilitySerializer


class BusinessAvailabilityDetailView(generics.RetrieveUpdateDestroyAPIView):
    # authentication_classes = (TokenAuthentication,)
    permission_classes = [IsAuthenticated]
    queryset = m.BusinessAvailability.objects.all()
    serializer_class = s.BusinessAvailabilitySerializer


class BusinessAccountListCreateView(generics.ListCreateAPIView):
    # authentication_classes = (TokenAuthentication,)
    # permission_classes = [IsAuthenticated]
    queryset = m.BusinessAccount.objects.all()
    serializer_class = s.BusinessAccountSerializer


class BusinessAccountDetailView(generics.RetrieveUpdateDestroyAPIView):
    # authentication_classes = (TokenAuthentication,)
    # permission_classes = [IsAuthenticated]
    queryset = m.BusinessAccount.objects.all()
    serializer_class = s.BusinessAccountSerializer


class BusinessCategoryListCreateView(generics.ListCreateAPIView):
    # authentication_classes = (TokenAuthentication,)
    # permission_classes = [AllowAny]
    queryset = m.BusinessCategory.objects.all()
    serializer_class = s.BusinessCategorySerializer


class BusinessCategoryDetailView(generics.RetrieveUpdateDestroyAPIView):
    # permission_classes = [IsAuthenticated]
    # authentication_classes = (TokenAuthentication,)
    queryset = m.BusinessCategory.objects.all()
    serializer_class = s.BusinessCategorySerializer


# End of Business APIs


class AddressListCreateView(generics.ListCreateAPIView):
    # permission_classes = (IsAuthenticated,)
    # authentication_classes = (TokenAuthentication,)
    queryset = m.Address.objects.all()
    serializer_class = s.AddressSerializer


class AddressDetailView(generics.RetrieveUpdateDestroyAPIView):
    # permission_classes = (IsAuthenticated,)
    # authentication_classes = (TokenAuthentication,)
    queryset = m.Address.objects.all()
    serializer_class = s.AddressSerializer


class AddressListCreateView(generics.ListCreateAPIView):
    # authentication_classes = (TokenAuthentication,)
    # permission_classes = [IsAuthenticated]
    queryset = m.Address.objects.all()
    serializer_class = s.AddressSerializer


class UserSearchAPIView(views.APIView):
    def get(self, request):
        query = request.query_params.get("query", "")

        if query:
            # Perform a case-insensitive search across relevant fields in the database
            results = User.objects.filter(
                Q(first_name__icontains=query)
                | Q(last_name__icontains=query)
                | Q(username__icontains=query)
            )
            serializer = UserSerializer(results, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response([], status=status.HTTP_200_OK)


def send_notification(user, message):
    # Create a new notification
    notification = m.Notification(user=user, message=message)
    notification.save()


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_notifications(request):
    user = request.user
    notifications = m.Notification.objects.filter(user=user, is_read=False).order_by(
        "-created_at"
    )
    serializer = s.NotificationSerializer(notifications, many=True)
    return Response(serializer.data)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def block_user(request):
    # Get the user who is doing the blocking
    blocker = request.user

    # Get the user who is being blocked (you can pass this user's ID or username in the request data)
    blocked_user_id = request.data.get("blocked_user_id")

    # Check if the block already exists
    existing_block = m.BlockedUser.objects.filter(
        blocker=blocker, blocked_user__id=blocked_user_id
    ).first()

    if existing_block:
        return Response(
            {"detail": "User is already blocked."}, status=status.HTTP_400_BAD_REQUEST
        )

    # Create a new block
    serializer = s.BlockedUserSerializer(
        data={"blocker": blocker.id, "blocked_user": blocked_user_id}
    )
    if serializer.is_valid():
        serializer.save()
        return Response(
            {"detail": "User blocked successfully."}, status=status.HTTP_201_CREATED
        )
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def list_blocked_users(request):
    # Get the authenticated user
    user = request.user

    # Retrieve the list of users they have blocked
    blocked_users = m.BlockedUser.objects.filter(blocker=user)

    # Serialize the blocked users data
    serializer = s.BlockedUserSerializer(blocked_users, many=True)

    return Response(serializer.data, status=status.HTTP_200_OK)


class EncryptionKeyAPIView(views.APIView):
    # authentication_classes = [TokenAuthentication]
    # permission_classes = [IsAuthenticated]

    def get(self, request):
        user = self.request.user
        # Adjust this as per your user model
        user_profile = m.UserProfile.objects.get(user=user)
        conversations = Conversation.objects.filter(participants=user_profile)

        # Create a dictionary to store encryption keys for each conversation
        encryption_keys = {}

        for conversation in conversations:
            encryption_key = conversation.get_encryption_key()
            if encryption_key:
                encryption_keys[conversation.id] = encryption_key.decode()

        return Response(encryption_keys, status=status.HTTP_200_OK)
