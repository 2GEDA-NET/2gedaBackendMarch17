from django.contrib.auth import get_user_model
from rest_framework import serializers

from user.auth.serializers import UserRegisterOnlySerializer

from . import models as m

User = get_user_model()


class BusinessCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = m.BusinessCategory
        fields = "__all__"


class PhoneNumberSerializer(serializers.ModelSerializer):
    class Meta:
        model = m.PhoneNumber
        exclude = ["business"]


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
    phone_number = PhoneNumberSerializer(write_only=True)
    category_id = serializers.IntegerField(required=True, write_only=True)

    class Meta:
        model = m.BusinessAccount
        exclude = ["category"]
        read_only_fields = ["is_verified"]

    def to_representation(self, instance):
        data = super().to_representation(instance)
        availability = m.BusinessDayAvailability.objects.filter(
            business=instance
        ).first()
        phone_number = m.PhoneNumber.objects.filter(business=instance).first()
        data["category"] = BusinessCategorySerializer(instance.category).data
        data["phone_number"] = PhoneNumberSerializer(phone_number).data
        data["availability"] = BusinessDayAvailabilitySerializer(availability).data
        return data

    def create(self, validated_data):
        phone_number = validated_data.pop("phone_number")
        user_data = validated_data.pop("user")
        category_id = validated_data.pop("category_id")
        availability = validated_data.pop("availability")
        category = m.BusinessCategory.objects.get(pk=category_id)
        business_user = User.objects.create_business_user(**user_data)
        business_account = m.BusinessAccount.objects.create(
            user=business_user, category=category, **validated_data
        )
        m.PhoneNumber.objects.create(business=business_account, **phone_number)

        availability_objects = {
            "monday": m.BusinessTimeAvailability.objects.create(
                **availability.get("monday")
            ),
            "tuesday": m.BusinessTimeAvailability.objects.create(
                **availability.get("tuesday")
            ),
            "wednesday": m.BusinessTimeAvailability.objects.create(
                **availability.get("wednesday")
            ),
            "thursday": m.BusinessTimeAvailability.objects.create(
                **availability.get("thursday")
            ),
            "friday": m.BusinessTimeAvailability.objects.create(
                **availability.get("friday")
            ),
            "saturday": m.BusinessTimeAvailability.objects.create(
                **availability.get("saturday")
            ),
            "sunday": m.BusinessTimeAvailability.objects.create(
                **availability.get("sunday")
            ),
        }

        m.BusinessDayAvailability.objects.create(
            business=business_account, **availability_objects
        )

        return business_account


class BusinessDocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = m.BusinessDocument
        fields = "__all__"


class BusinessOwnerProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = m.BusinessOwnerProfile
        exclude = ["profile", "is_verified"]
