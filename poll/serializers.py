from rest_framework import serializers

from . import models as m


class PollOptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = m.PollOption
        fields = ["id", "content"]

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data["votes"] = instance.voters.count()
        return data


class WriteOnlyPollOptionSerializer(serializers.Serializer):
    option_id = serializers.IntegerField(required=True)


class PollSerializer(serializers.ModelSerializer):
    options = serializers.ListField(
        child=PollOptionSerializer(), write_only=True, required=True
    )

    class Meta:
        model = m.Poll
        fields = "__all__"
        read_only_fields = ["is_closed", "creator"]

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data["options"] = PollOptionSerializer(instance.options.all(), many=True).data
        data["creator"] = {
            "id": instance.creator.user.id,
            "first_name": instance.creator.user.first_name,
            "last_name": instance.creator.user.last_name,
            "username": instance.creator.user.username,
            "email": instance.creator.user.email,
            "phone_number": instance.creator.user.phone_number,
        }
        return data

    def create(self, validated_data):
        options = validated_data.pop("options", [])
        poll = m.Poll.objects.create(**validated_data)
        for option in options:
            m.PollOption.objects.create(poll=poll, **option)
        return poll


# from rest_framework import serializers
# from .models import *

# class OptionSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Option
#         fields = '__all__'

# class VoteSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Vote
#         fields = '__all__'

# class PollSerializer(serializers.ModelSerializer):
#     count_views = serializers.SerializerMethodField()


#     class Meta:
#         model = Poll
#         fields = '__all__'

#     def get_count_views(self, obj):
#         return obj.count_views()


#     def create(self, validated_data):
#         # Ensure that the user who creates the poll is the request user
#         validated_data['user'] = self.context['request'].user
#         return super(PollSerializer, self).create(validated_data)


# class SuggestedPollSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Poll
#         fields = '__all__'


# class AccessRequestSerializer(serializers.Serializer):
#     poll_id = serializers.PrimaryKeyRelatedField(queryset=Poll.objects.all())

#     def create(self, validated_data):
#         user = self.context['request'].user
#         poll = validated_data['poll']

#         # Check if the user has already voted or requested access
#         if user in poll.voters.all() or user in poll.access_requests.all():
#             raise serializers.ValidationError("You have already voted or requested access to this poll.")

#         return {'user': user, 'poll': poll}


# class AccessApprovalSerializer(serializers.Serializer):
#     poll_id = serializers.PrimaryKeyRelatedField(queryset=Poll.objects.all())
#     user_id = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
#     approval_status = serializers.BooleanField()

#     def create(self, validated_data):
#         user = self.context['request'].user
#         poll = validated_data['poll']
#         target_user = validated_data['user_id']
#         approval_status = validated_data['approval_status']

#         # Check if the user is the creator of the poll
#         if user != poll.user:
#             raise serializers.ValidationError("You do not have permission to approve/deny access requests.")

#         # Check if the poll is private
#         if poll.type != 'Private':
#             raise serializers.ValidationError("Access requests can only be handled for private polls.")

#         return {'poll': poll, 'user': target_user, 'approval_status': approval_status}


# class PollCreateSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Poll
#         fields = ('question', 'options', 'duration', 'type', 'media')

# class PaymentSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Payment
#         fields = '__all__'

# class PollResultsSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Poll
#         fields = ['id', 'question', 'options', 'type', 'created_at', 'is_active', 'is_ended', 'vote_count']
