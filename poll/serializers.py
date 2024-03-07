from rest_framework import serializers

from user.account.serializers import UserProfileMinimalSerializer

from . import models as m


class PollOptionSerializer(serializers.ModelSerializer):

    class Meta:
        model = m.PollOption
        fields = ["id", "content"]

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data["votes"] = instance.voters.count()
        data["voters"] = UserProfileMinimalSerializer(
            instance.voters.all(), many=True
        ).data
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
        read_only_fields = ["creator", "created_at", "updated_at", "is_closed"]

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data["options"] = PollOptionSerializer(instance.options.all(), many=True).data
        data["total_votes"] = sum(
            vote.voters.count() for vote in instance.options.all()
        )
        data["creator"] = (
            {
                "id": instance.creator.user.id,
                "first_name": instance.creator.user.first_name,
                "last_name": instance.creator.user.last_name,
                "username": instance.creator.user.username,
                "email": instance.creator.user.email,
                "phone_number": instance.creator.user.phone_number,
                "profile_picture": instance.creator.profile_image,
            }
            if instance.creator
            else None
        )
        return data

    def update(self, instance, validated_data):
        options = validated_data.pop("options", [])
        for option in options:
            # update the option if exists otherwise create new option for the poll instance
            poll_option = m.PollOption.objects.filter(
                poll=instance, content=option.get("content", "")
            )
            if poll_option.exists():
                poll_option.update(**option)
            else:
                m.PollOption.objects.create(poll=instance, **option)
        polls = m.Poll.objects.filter(pk=instance.id)
        polls.update(**validated_data)
        return polls.first()

    def create(self, validated_data):
        options = validated_data.pop("options", [])
        poll = m.Poll.objects.create(**validated_data)
        for option in options:
            m.PollOption.objects.create(poll=poll, **option)
        return poll
