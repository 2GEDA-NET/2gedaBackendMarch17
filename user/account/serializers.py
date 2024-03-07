from django.contrib.auth import get_user_model
from rest_framework import serializers

from ..auth.serializers import ReadOnlyUserSerializer
from . import models as m

User = get_user_model()


class UserAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = m.UserAddress
        exclude = ("profile",)


class WriteOnlyUserAddressSerializer(serializers.Serializer):
    country = serializers.CharField(required=True)
    state = serializers.CharField(required=True)
    city = serializers.CharField(required=True)
    street_address = serializers.CharField(required=True)
    zip_code = serializers.CharField(required=True)


class UserProfileSerializer(serializers.ModelSerializer):
    user = ReadOnlyUserSerializer(read_only=True)
    address = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = m.UserProfile
        exclude = ["stickers", "sticking"]

    def get_address(self, profile):
        address = m.UserAddress.objects.filter(
            profile=self.context["request"].user.profile
        )
        return UserAddressSerializer(address).data

    def to_representation(self, instance):
        data = super().to_representation(instance)
        address = m.UserAddress.objects.filter(profile=instance)
        data["user"] = ReadOnlyUserSerializer(instance.user).data
        data["address"] = UserAddressSerializer(address.first()).data
        data["stickers"] = instance.stickers.count()
        data["sticking"] = instance.sticking.count()
        return data

    def create(self, validated_data):
        address = validated_data.get("address", None)
        if address:
            m.UserAddress.objects.create(
                profile=self.context["request"].user.profile, **address
            )
        return super().create(validated_data)


class UserProfileMinimalSerializer(serializers.ModelSerializer):

    username = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = m.UserProfile
        fields = ["id", "username", "profile_picture"]

    def get_username(self, instance):
        return instance.user.username


class WriteOnlyUserProfileSerializer(serializers.Serializer):
    first_name = serializers.CharField(required=False)
    last_name = serializers.CharField(required=False)


class UserProfileUpdateSerializer(UserProfileSerializer):
    user = WriteOnlyUserProfileSerializer(required=True)
    address = UserAddressSerializer(write_only=True, required=True)

    class Meta(UserProfileSerializer.Meta):
        read_only_fields = ["media", "is_flagged"]
