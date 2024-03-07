from django.db.models import Q
from django.utils import timezone
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status, views, viewsets
from rest_framework.authtoken.models import Token
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

# from ..account.models import User
from . import models as m
from . import serializers as s


class UserRegistrationAPI(views.APIView):
    """Registration API View"""

    permission_classes = [AllowAny]

    @swagger_auto_schema(
        request_body=s.UserRegistrationSerializer,
        responses={201: s.UserRegistrationSerializer},
    )
    def post(self, request, *args, **kwargs):
        response = {}
        status_code = None
        serializer = s.UserRegistrationSerializer(
            data=request.data, context={"request": request}
        )
        if serializer.is_valid():
            serializer.save()
            response["message"] = "Registration successful."
            response["status"] = True
            response["data"] = serializer.data
            status_code = status.HTTP_201_CREATED
        else:
            response["message"] = "User registration fail."
            response["status"] = False
            response["data"] = serializer.errors
            status_code = status.HTTP_400_BAD_REQUEST
        return Response(response, status=status_code)


class UserLoginAPI(views.APIView):
    """Login API View"""

    permission_classes = [AllowAny]

    request_body = openapi.Schema(
        title="Login API",
        type=openapi.TYPE_OBJECT,
        properties={
            "email": openapi.Schema(
                type=openapi.TYPE_STRING,
                format=openapi.FORMAT_EMAIL,
                description="Email address",
            ),
            "password": openapi.Schema(
                type=openapi.TYPE_STRING, format="string", description="Password"
            ),
        },
        required=["email", "password"],
    )

    @swagger_auto_schema(
        request_body=request_body, responses={200: s.UserLoginSerializer}
    )
    def post(self, request, *args, **kwargs):
        email = request.data.get("email", "").lower().strip()
        user = m.User.objects.filter(Q(email=email) | Q(username=email))
        password = request.data.get("password")

        response = {}
        status_code = None

        if user.exists() and user.first().check_password(password):
            serializer = s.UserLoginSerializer(data=request.data)
            if serializer.is_valid():
                user = user.first()
                response["message"] = "User login successful."
                response["status"] = True
                response["data"] = serializer.data
                status_code = status.HTTP_200_OK
                user.last_login = timezone.now()
                user.save()
            else:
                response["message"] = "Login fail."
                response["status"] = False
                response["data"] = serializer.errors
                status_code = status.HTTP_400_BAD_REQUEST
            return Response(response, status=status_code)
        else:
            response["message"] = "Incorrect credentials."
            response["status"] = False
            status_code = status.HTTP_401_UNAUTHORIZED
            return Response(response, status=status_code)


class AuthenticationViewSet(viewsets.GenericViewSet):
    """Authentication viewset"""

    user_response = openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            "message": openapi.Schema(type=openapi.TYPE_STRING, format="string")
        },
    )
    params = [
        openapi.Parameter(
            name="verification_type",
            in_=openapi.IN_QUERY,
            type=openapi.TYPE_STRING,
            description="*NOTE*: `account_verification` for new user "
            "and `password_reset` for user password reset.",
            enum=["account_verification", "password_reset"],
            required=True,
        )
    ]

    def get_permissions(self):
        if self.action in ["change_password", "get_otp", "delete_account"]:
            permissions = [IsAuthenticated]
        else:
            permissions = [AllowAny]
        return [permission() for permission in permissions]

    @swagger_auto_schema(
        request_body=s.UserChangePasswordSerializer, responses={200: user_response}
    )
    @action(methods=["POST"], detail=False, url_path="change-password")
    def change_password(self, request, *args, **kwargs):
        """Change password"""
        user = self.request.user
        response = {}
        if not user.check_password(request.data.get("old_password")):
            response["status"] = False
            response["message"] = "Incorrect old password."
            status_code = status.HTTP_401_UNAUTHORIZED
        else:
            serializer = s.UserChangePasswordSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            user.set_password(serializer.validated_data.get("new_password"))
            print("User: ", user)
            user.save()
            response["status"] = True
            response["message"] = "Password changed successfully"
            status_code = status.HTTP_200_OK
        return Response(response, status=status_code)

    @swagger_auto_schema(
        request_body=s.OneTimePasswordSerializer, responses={200: user_response}
    )
    @action(methods=["POST"], detail=False, url_path="forgot-password")
    def forgot_password(self, request, *args, **kwargs):
        """Forgot password"""
        email = request.data.get("email", "").lower().strip()
        user = m.User.objects.filter(email=email)
        if user.exists():
            user = user.first()
            otp = user.generate_otp()
            m.OneTimePassword.objects.create(
                user=user, otp=otp, verification_type="password_reset"
            ).send_code()
            return Response(
                {"message": "Password reset email sent.", "status": True},
                status=status.HTTP_200_OK,
            )
        return Response(
            {"message": "No user with this email.", "status": False},
            status=status.HTTP_400_BAD_REQUEST,
        )

    @swagger_auto_schema(
        request_body=s.UserResetPasswordSerializer, responses={200: user_response}
    )
    @action(methods=["POST"], detail=False, url_path="reset-password")
    def reset_password(self, request, *args, **kwargs):
        """Reset password"""
        otp = request.data.get("otp", "")
        email = request.data.get("email", "").lower().strip()
        user = m.User.objects.filter(email=email)
        if not user.exists():
            return Response(
                {"message": "User with this email does not exist", "status": False},
                status=status.HTTP_400_BAD_REQUEST,
            )
        user = user.first()
        if not user.check_otp(otp):
            return Response(
                {"message": "Incorrect OTP", "status": False},
                status=status.HTTP_400_BAD_REQUEST,
            )
        user.set_password(request.data.get("password"))
        user.save()
        return Response(
            {"message": "Password reset successful", "status": True},
            status=status.HTTP_200_OK,
        )

    @swagger_auto_schema(responses={200: user_response}, manual_parameters=params)
    @action(methods=["GET"], detail=False, url_path="resend-otp")
    def get_otp(self, request, *args, **kwargs):
        """Get OTP

        verification_type: `account_verification` for new user
        and `password_verification` user password reset.

        """
        verification_type = request.GET.get("verification_type")
        if not verification_type and verification_type not in [
            "account_verification",
            "password_reset",
        ]:
            return Response(
                {
                    "message": "Must provide verification_type params: "
                    "account_verification or password_reset."
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
        if request.user.is_verified:
            return Response(
                {"message": "User already verified."}, status=status.HTTP_302_FOUND
            )
        otp, _ = m.OneTimePassword.objects.get_or_create(
            user=request.user,
        )
        otp.otp = request.user.generate_otp()
        otp.verification_type = verification_type
        otp.save()
        otp.send_code()
        return Response(
            {"message": "Verification code sent successfully", "status": True},
            status=status.HTTP_200_OK,
        )

    @action(methods=["DELETE"], detail=False, url_path="delete-account")
    def delete_account(self, request, *args, **kwargs):
        current_user = m.User.objects.filter(id=request.user.id)
        current_user.delete()
        return Response(
            {"message": "User account deleted", "status": True},
            status=status.HTTP_200_OK,
        )

    @swagger_auto_schema(
        request_body=s.OneTimePasswordSerializer, responses={200: user_response}
    )
    @action(methods=["POST"], detail=False, url_path="get-token")
    def get_token(self, request, *args, **kwargs):
        email = request.data.get("email", "").lower().strip()
        auth_user = m.User.objects.filter(email=email)
        if auth_user.exists():
            token, _ = Token.objects.get_or_create(user=auth_user.first())
            return Response({"token": token.key}, status=status.HTTP_200_OK)
        return Response(
            {"message": "No user with this email."}, status=status.HTTP_400_BAD_REQUEST
        )

    @swagger_auto_schema(
        request_body=s.UserEmailVerifySerializer, responses={200: user_response}
    )
    @action(methods=["POST"], detail=False, url_path="verify-account")
    def verify_account(self, request, *args, **kwargs):
        email = request.data.get("email", "").lower().strip()
        auth_user = m.User.objects.filter(email=email)

        if auth_user.exists():
            user = auth_user.first()
            if not user.check_otp(request.data.get("otp")):
                return Response(
                    {"message": "Invalid OTP code.", "status": False},
                    status=status.HTTP_403_FORBIDDEN,
                )
            if user.is_verified:
                return Response(
                    {"message": "You're already been verified."},
                    status=status.HTTP_302_FOUND,
                )
            user.is_verified = True
            user.save()
            return Response(
                {
                    "message": "Your email has been verified successfully.",
                    "status": True,
                },
                status=status.HTTP_200_OK,
            )
        return Response(
            {"message": "No user with this email."}, status=status.HTTP_400_BAD_REQUEST
        )
