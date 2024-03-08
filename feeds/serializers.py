from django.db import IntegrityError
from django.dispatch import receiver
from rest_framework import serializers

from . import models as m

from utils.exception import BadRequestException


class PostFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = m.PostFile
        fields = ("file",)

    def create(self, validated_data):

        post = self.context["post"]

        file_type = self.context["file_type"]

        instance = m.PostFile.objects.create(
            post=post, file_type=file_type, **validated_data
        )

        return instance




class CommentFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = m.CommentFile
        fields = ("file",)

    def create(self, validated_data):

        comment = self.context["comment"]

        file_type = self.context["file_type"]

        instance = m.CommentFile.objects.create(
            comment=comment, file_type=file_type, **validated_data
        )

        return instance




class PostSerializer(serializers.ModelSerializer):
    file = PostFileSerializer(required=False, allow_null=True)
    hashtags = serializers.ListSerializer(child=serializers.CharField(), required=False)
    tagged_users = serializers.ListField(required=False)

    class Meta:
        model = m.Post
        fields = (
            "text_content",
            "file",
            "location",
            "hashtags",
            "is_business_post",
            "is_personal_post",
            "tagged_users",
        )

    def create(self, validated_data):

        user = self.context["user"]

        tagged_users_data = validated_data.pop("tagged_users", [])

        hashtags_data = validated_data.pop("hashtags", [])

        new_hashtags = [
            m.Hashtag.objects.get_or_create(name=name)[0].id for name in hashtags_data
        ]

        try:
            instance = m.Post.objects.create(user=user, **validated_data)
            instance.tagged_users.set(tagged_users_data)
            instance.hashtags.set(new_hashtags)

        except IntegrityError as e:

            raise BadRequestException(
                "One or more user IDs in the tagged users do not exist"
            )

        return instance


class CommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = m.Comment
        fields = (
            "text_content",
        )

    def create(self, validated_data):

        post: m.Post = self.context["post"]

        user = self.context["user"]

        instance = m.Comment.objects.create(user=user, post=post, **validated_data)

        post.comments.add(instance)

        return instance


class ReactionPostSerializer(serializers.ModelSerializer):

    class Meta:
        model = m.PostReaction
        fields = ("reaction_type",)

    def create(self, validated_data):

        post = self.context["post"]

        user = self.context["user"]

        instance = m.PostReaction.objects.create(user=user, post=post, **validated_data)

        return instance


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = m.User
        fields = ("id",)


class ReportPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = m.ReportPost
        fields = (
            "post",
            "reason",
        )

    def create(self, validated_data):

        user = self.context["user"]

        instance = m.ReportPost.objects.create(user=user, **validated_data)

        return instance


class ReturnPostSerializer(serializers.ModelSerializer):
    file = PostFileSerializer(required=False, allow_null=True)
    hashtags = serializers.ListSerializer(child=serializers.CharField(), required=False)

    tagged_users = UserSerializer(required=False, read_only=True)

    class Meta:
        model = m.Post
        fields = (
            "text_content",
            "file",
            "location",
            "hashtags",
            "is_business_post",
            "is_personal_post",
            "tagged_users",
        )


class StatusSerializer(serializers.ModelSerializer):
    tagged_users = serializers.ListField(required=False)

    class Meta:
        model = m.Status
        fields = ("caption", "file", "tagged_users")

    def create(self, validated_data):

        user = self.context["user"]

        tagged_users_data = list(
            map(int, validated_data.pop("tagged_users", [])[0].split(", "))
        )

        instance = m.Status.objects.create(user=user, **validated_data)

        try:
            instance.tagged_users.set(tagged_users_data)

        except IntegrityError as e:
            raise BadRequestException(
                "One or more user IDs in the tagged users do not exist"
            )

        return instance
