import base64
import secrets

from rest_framework import serializers
from rest_framework.authtoken.models import Token

from notifications import send_verification_code

from .models import User, OneTimePassword


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

        if user.exists():
            raise serializers.ValidationError("User with this email already exist")

        user = User.objects.create_user(**validated_data)
        user.secret_key = base64.b32encode(secrets.token_bytes(10)).decode("utf-8")
        # user.otp = otp_code
        user.auth_token = Token.objects.create(user=user)
        self.token = user.auth_token.key
        user.save()

        # Send email
        print("Sending Verification Code......")
        otp_code = user.generate_otp()
        OneTimePassword.objects.create(
            user=user, otp=otp_code, verification_type="account_verification"
        ).send_code()

        return user


class UserLoginSerializer(serializers.Serializer):
    """Login user serializer class"""

    user = UserSerializer(read_only=True)
    email = serializers.EmailField(required=True, write_only=True)
    password = serializers.CharField(required=True, write_only=True)

    def to_representation(self, instance):
        data = super().to_representation(instance)
        user = User.objects.get(email=self.validated_data.get("email"))
        data["user"] = UserSerializer(user).data
        data["token"] = Token.objects.get_or_create(user=user)[0].key
        data["last_login"] = user.last_login
        return data

    def validate_email(self, email):
        email = email or ""
        user = User.objects.filter(email=email.lower().strip())
        if not user.exists():
            raise serializers.ValidationError("User with this email does not exist")
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
