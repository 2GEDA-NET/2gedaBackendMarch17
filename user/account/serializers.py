from django.contrib.auth import get_user_model
from rest_framework import serializers

from ..auth.serializers import WriteOnlyUserSerializer
from . import models as m

User = get_user_model()


class AddressSerializer(serializers.ModelSerializer):
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
    user = WriteOnlyUserSerializer(read_only=True)
    address = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = m.UserProfile
        fields = "__all__"

    def get_address(self, profile):
        address = m.UserAddress.objects.filter(
            profile=self.context["request"].user.profile
        )
        return AddressSerializer(address).data

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data["stickers_count"] = instance.stickers_count
        data["sticking_count"] = instance.sticking_count
        return data

    def update(self, instance, validated_data):
        data = validated_data
        user_email = data.pop("user", {}).get("email")
        user_address = data.pop("address", {})
        user = User.objects.filter(email=user_email)
        if user.exists():
            user.update(**data.get("user"))
        if user_address:
            m.UserAddress.objects.filter(
                profile=self.context["request"].user.profile
            ).update(**user_address)
        return super().update(instance, data)

    def create(self, validated_data):
        address = validated_data.get("address", None)
        if address:
            m.UserAddress.objects.create(
                profile=self.context["request"].user.profile, **address
            )
        return super().create(validated_data)


class WriteOnlyUserProfileSerializer(serializers.Serializer):
    first_name = serializers.CharField(required=False)
    last_name = serializers.CharField(required=False)


class UserProfileUpdateSerializer(serializers.ModelSerializer):
    """User profile update serializer"""

    user = WriteOnlyUserProfileSerializer(required=True)
    address = AddressSerializer(write_only=True, required=True)

    class Meta:
        model = m.UserProfile
        fields = "__all__"
        read_only_fields = ["media", "is_flagged"]


# class ReportUserSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = m.ReportedUser
#         fields = ["user", "description"]


# class ReportedUserSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = m.ReportedUser
#         fields = "__all__"


# # class UserProfileSerializer(serializers.ModelSerializer):
# #     class Meta:
# #         model = UserProfile
# #         fields = '__all__'


# class BusinessCategorySerializer(serializers.ModelSerializer):
#     class Meta:
#         model = m.BusinessCategory
#         fields = [
#             "name",
#         ]


# class AddressSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = m.Address
#         fields = "__all__"


# class CurrentCityAddressSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = (
#             m.Address
#         )  # Replace 'Address' with the actual name of your Address model
#         fields = ("current_city",)


# class BusinessAvailabilitySerializer(serializers.ModelSerializer):
#     class Meta:
#         model = m.BusinessAvailability
#         fields = "__all__"


# class BusinessAccountSerializer(serializers.ModelSerializer):
#     business_availability = BusinessAvailabilitySerializer()
#     address = CurrentCityAddressSerializer()
#     # Include the BusinessCategorySerializer
#     business_category = BusinessCategorySerializer()

#     class Meta:
#         model = m.BusinessAccount
#         fields = "__all__"

#     def create(self, validated_data):
#         business_availability_data = validated_data.pop("business_availability")
#         address_data = validated_data.pop("address")
#         business_category_data = validated_data.pop(
#             "business_category"
#         )  # Extract business category data

#         business_availability = m.BusinessAvailability.objects.create(
#             **business_availability_data
#         )
#         address = m.Address.objects.create(**address_data)
#         business_category = m.BusinessCategory.objects.create(
#             **business_category_data
#         )  # Create business category

#         business_profile = m.BusinessAccount.objects.create(
#             business_availability=business_availability,
#             address=address,
#             business_category=business_category,  # Assign business category
#             **validated_data,
#         )

#         return business_profile

#     def update(self, instance, validated_data):
#         business_availability_data = validated_data.get("business_availability", {})

#         # Days of the week
#         days_of_week = [
#             "sunday",
#             "monday",
#             "tuesday",
#             "wednesday",
#             "thursday",
#             "friday",
#             "saturday",
#         ]

#         # Loop through days of the week and update fields
#         for day in days_of_week:
#             setattr(
#                 instance.business_availability,
#                 day,
#                 business_availability_data.get(
#                     day, getattr(instance.business_availability, day)
#                 ),
#             )
#             setattr(
#                 instance.business_availability,
#                 f"{day}_open",
#                 business_availability_data.get(
#                     f"{day}_open",
#                     getattr(instance.business_availability, f"{day}_open"),
#                 ),
#             )
#             setattr(
#                 instance.business_availability,
#                 f"{day}_close",
#                 business_availability_data.get(
#                     f"{day}_close",
#                     getattr(instance.business_availability, f"{day}_close"),
#                 ),
#             )

#         # Update other fields as before
#         instance.year_founded = validated_data.get(
#             "year_founded", instance.year_founded
#         )

#         # Update the related Address instance
#         address_data = validated_data.get("address", {})
#         address = instance.address
#         address.city = address_data.get("city", address.city)

#         # Update the related BusinessCategory instance
#         business_category_data = validated_data.get("business_category", {})
#         business_category = instance.business_category
#         business_category.name = business_category_data.get(
#             "name", business_category.name
#         )

#         instance.save()
#         instance.business_availability.save()
#         instance.address.save()
#         instance.business_category.save()

#         return instance

#     def to_representation(self, instance):
#         """
#         Customize the representation of the BusinessProfile instance.
#         Include sub-fields in the output.
#         """
#         ret = super().to_representation(instance)
#         ret["business_availability"] = BusinessAvailabilitySerializer(
#             instance.business_availability
#         ).data
#         ret["address"] = CurrentCityAddressSerializer(instance.address).data
#         ret["business_category"] = BusinessCategorySerializer(
#             instance.business_category
#         ).data
#         return ret


#     # class UserProfileSerializer(serializers.ModelSerializer):
#     #     stickers = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
#     #     sticking = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
#     #     stickers_count = serializers.SerializerMethodField()
#     #     sticking_count = serializers.SerializerMethodField()
#     #     address = CurrentCityAddressSerializer()

#     class Meta:
#         model = m.UserProfile
#         fields = (
#             "work",
#             "date_of_birth",
#             "gender",
#             "custom_gender",
#             "address",
#             "stickers",
#             "sticking",
#             "stickers_count",
#             "sticking_count",
#         )

#     def get_stickers_count(self, obj):
#         return obj.sticker_count()

#     def get_sticking_count(self, obj):
#         return obj.sticking_count()


# class UserProfileUpdateSerializer(serializers.ModelSerializer):
#     profile = UserProfileSerializer()

#     class Meta:
#         model = User
#         fields = ("first_name", "last_name", "username", "password", "profile")

#     extra_kwargs = {
#         # Password field should be write-only
#         "password": {"write_only": True},
#     }

#     def update(self, instance, validated_data):
#         # Update User fields
#         instance.first_name = validated_data.get("first_name", instance.first_name)
#         instance.last_name = validated_data.get("last_name", instance.last_name)
#         instance.username = validated_data.get("username", instance.username)
#         if "password" in validated_data:
#             instance.set_password(validated_data["password"])

#         # Update UserProfile fields
#         profile_data = validated_data.get("profile", {})
#         profile = instance.profile

#         profile.work = profile_data.get("work", profile.work)
#         profile.date_of_birth = profile_data.get("date_of_birth", profile.date_of_birth)
#         profile.gender = profile_data.get("gender", profile.gender)
#         profile.custom_gender = profile_data.get("custom_gender", profile.custom_gender)

#         # Update Address fields (including current city)
#         address_data = profile_data.get("address", {})
#         address = profile.address

#         address.current_city = address_data.get("current_city", address.current_city)

#         # Save both User, UserProfile, and Address instances
#         instance.save()
#         profile.save()
#         address.save()

#         return instance


# class UserListSerializer(serializers.ModelSerializer):
#     sticking_count = serializers.SerializerMethodField()
#     sticker_count = serializers.SerializerMethodField()

#     class Meta:
#         model = User
#         fields = ("first_name", "last_name", "sticking_count", "sticker_count")

#     def get_sticking_count(self, obj):
#         try:
#             user_profile = m.UserProfile.objects.get(user=obj)
#             return user_profile.sticking.count()
#         except m.UserProfile.DoesNotExist:
#             return 0

#     def get_sticker_count(self, obj):
#         try:
#             user_profile = m.UserProfile.objects.get(user=obj)
#             return user_profile.stickers.count()
#         except m.UserProfile.DoesNotExist:
#             return 0
