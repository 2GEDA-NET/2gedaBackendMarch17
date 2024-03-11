from django.contrib.auth import get_user_model
from rest_framework import serializers

from authentication.serializers import UserRegisterOnlySerializer

from . import models as m

User = get_user_model()


class BusinessTimeAvailabilitySerializer(serializers.ModelSerializer):
    class Meta:
        model = m.BusinessTimeAvailability
        fields = "__all__"


class BusinessDayAvailabilitySerializer(serializers.ModelSerializer):
    monday = BusinessTimeAvailabilitySerializer(required=True)
    tuesday = BusinessTimeAvailabilitySerializer(required=True)
    wednesday = BusinessTimeAvailabilitySerializer(required=True)
    thursday = BusinessTimeAvailabilitySerializer(required=True)
    friday = BusinessTimeAvailabilitySerializer(required=True)
    saturday = BusinessTimeAvailabilitySerializer(required=True)
    sunday = BusinessTimeAvailabilitySerializer(required=True)

    class Meta:
        model = m.BusinessDayAvailability
        exclude = ["business"]


class BusinessAccountSerializer(serializers.ModelSerializer):
    availability = BusinessDayAvailabilitySerializer(write_only=True)
    user = UserRegisterOnlySerializer(required=True)

    class Meta:
        model = m.BusinessAccount
        fields = "__all__"
        read_only_fields = ["is_verified", "profile"]

    def to_representation(self, instance):
        data = super().to_representation(instance)
        # data["user"] = BusinessUserRegisterOnlySerializer(instance.user).data
        availability = m.BusinessDayAvailability.objects.filter(
            business=instance
        ).first()
        data["availability"] = BusinessDayAvailabilitySerializer(availability).data
        return data

    def create(self, validated_data):
        user_data = validated_data.pop("user", {})
        availability = validated_data.pop("availability", {})
        business_user = User.objects.create_business_user(**user_data)
        business_account = m.BusinessAccount.objects.create(
            user=business_user, **validated_data
        )
        availability_objects = {
            "monday": m.BusinessTimeAvailability.objects.create(
                **availability.get("monday", {})
            ),
            "tuesday": m.BusinessTimeAvailability.objects.create(
                **availability.get("tuesday", {})
            ),
            "wednesday": m.BusinessTimeAvailability.objects.create(
                **availability.get("wednesday", {})
            ),
            "thursday": m.BusinessTimeAvailability.objects.create(
                **availability.get("thursday", {})
            ),
            "friday": m.BusinessTimeAvailability.objects.create(
                **availability.get("friday", {})
            ),
            "saturday": m.BusinessTimeAvailability.objects.create(
                **availability.get("saturday", {})
            ),
            "sunday": m.BusinessTimeAvailability.objects.create(
                **availability.get("sunday", {})
            ),
        }

        m.BusinessDayAvailability.objects.create(
            business=business_account, **availability_objects
        )

        return business_account


class BusinessVerificationSerializer(serializers.ModelSerializer):
    business_id = serializers.IntegerField(required=True, write_only=True)

    class Meta:
        model = m.BusinessVerification
        exclude = ["business"]
        read_only_fields = ["is_completed"]

    def create(self, validated_data):
        business_id = int(validated_data.pop("business_id", 0))
        business = m.BusinessAccount.objects.filter(pk=business_id)
        if not business.exists():
            raise serializers.ValidationError({"message": "Invalid business id."})
        return m.BusinessVerification.objects.create(
            business=business.first(), **validated_data
        )
