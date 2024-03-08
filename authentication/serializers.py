import base64
import secrets

from django.db.models import Q
from rest_framework import serializers
from rest_framework.authtoken.models import Token

from .models import OneTimePassword, User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "email",
            "phone_number",
            "is_verified",
            "password",
        )
        extra_kwargs = {
            "password": {"write_only": True},
            "is_verified": {"read_only": True},
        }


class ReadOnlyUserSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    first_name = serializers.CharField(read_only=True)
    last_name = serializers.CharField(read_only=True)
    email = serializers.EmailField(required=True)
    phone_number = serializers.CharField(read_only=True)
    is_verified = serializers.BooleanField(read_only=True)


class UserRegisterOnlySerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    username = serializers.CharField(required=True)
    phone_number = serializers.CharField(required=False)
    password = serializers.CharField(required=True, write_only=True)

    def validate(self, attrs):
        email = attrs.get("email", "")
        username = attrs.get("username", "")
        phone_number = attrs.get("phone_number", "")
        user = User.objects.filter(
            Q(email=email) | Q(username=username) | Q(phone_number=phone_number)
        )
        if user.exists():
            raise serializers.ValidationError("User already exist!")
        return attrs


class UserRegistrationSerializer(UserSerializer):
    """Serializer registration class for all users"""

    token = serializers.CharField(read_only=True)

    class Meta(UserSerializer.Meta):
        fields = UserSerializer.Meta.fields + ("token",)

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data["token"] = self.token
        return data

    def create(self, validated_data):
        email = validated_data.get("email", "")
        user = User.objects.filter(email=email.lower().strip())

        # Check if user exist.
        if user.exists():
            raise serializers.ValidationError("User with this email already exist")

        user = User.objects.create_user(**validated_data)
        user.secret_key = base64.b32encode(secrets.token_bytes(10)).decode("utf-8")
        user.auth_token = Token.objects.create(user=user)
        self.token = user.auth_token.key
        user.save()

        # Generate and send the otp to email
        otp_code = user.generate_otp()
        OneTimePassword.objects.create(
            user=user,
            otp=otp_code,
            verification_type="account_verification",
        ).send_code()

        return user


class UserLoginSerializer(serializers.Serializer):
    """Login user serializer class"""

    user = UserSerializer(read_only=True)
    email = serializers.CharField(required=True, write_only=True)
    password = serializers.CharField(required=True, write_only=True)

    def to_representation(self, instance):
        data = super().to_representation(instance)
        email = self.validated_data.get("email", "").lower().strip()
        user = User.objects.get(Q(email=email) | Q(username=email))
        data["user"] = UserSerializer(user).data
        data["token"] = Token.objects.get_or_create(user=user)[0].key
        data["last_login"] = user.last_login
        return data

    def validate_email(self, email):
        email = email.lower().strip() or ""
        user = User.objects.filter(Q(email=email) | Q(username=email))
        if not user.exists():
            raise serializers.ValidationError("User does not exist")
        return email


class UserChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)


class OneTimePasswordSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)


class UserEmailVerifySerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    otp = serializers.CharField(required=True)


class UserResetPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    otp = serializers.CharField(required=True, max_length=6)
    password = serializers.CharField(required=True)


class UserDeletionSerializer(serializers.Serializer):
    reason_choice = serializers.CharField(write_only=True, required=False)
    reason = serializers.CharField(write_only=True, required=False)
    password = serializers.CharField(write_only=True, required=True)
