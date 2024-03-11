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
        fields = ("text_content",)

    def create(self, validated_data):

        post: m.Post = self.context["post"]

        user = self.context["user"]

        file = self.context.get("file")

        if file:
            file_serializer = CommentFileSerializer(data={"file": file})
            if not file_serializer.is_valid():
                raise BadRequestException(
                    message=file_serializer.error_messages, data=file_serializer.errors
                )

        comment_instance = m.Comment.objects.create(
            user=user, post=post, **validated_data
        )

        post.comments.add(comment_instance)

        if file:
            comment_file_instance = m.CommentFile.objects.create(
                comment=comment_instance, file=file, file_type=file.content_type
            )

            comment_instance.file = comment_file_instance

            comment_instance.save()

        return comment_instance


class ReactionPostSerializer(serializers.ModelSerializer):

    class Meta:
        model = m.PostReaction
        fields = ("reaction_type",)

    def create(self, validated_data):

        post = self.context["post"]

        user = self.context["user"]

        instance = m.PostReaction.objects.create(user=user, post=post, **validated_data)

        return instance


class ReactionCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = m.CommentReaction
        fields = ("reaction_type",)

    def create(self, validated_data):

        comment = self.context["comment"]

        user = self.context["user"]

        instance = m.CommentReaction.objects.create(
            user=user, comment=comment, **validated_data
        )

        return instance


class ReactionReplySerializer(serializers.ModelSerializer):
    class Meta:
        model = m.ReplyReaction
        fields = ("reaction_type",)

    def create(self, validated_data):

        reply = self.context["reply"]

        user = self.context["user"]

        instance = m.ReplyReaction.objects.create(
            user=user, reply=reply, **validated_data
        )

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


class ReplyCommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = m.Reply
        fields = ("text_content",)

    def create(self, validated_data):

        comment: m.Comment = self.context["comment"]

        user = self.context["user"]

        reply_instance = m.Reply.objects.create(
            comment=comment, user=user, **validated_data
        )

        reply_instance.save()

        return reply_instance


class RepostSerializer(serializers.Serializer):
    hashtags = serializers.ListSerializer(child=serializers.CharField(), required=False)
    tagged_users = serializers.ListField(required=False)

    class Meta:
        model = m.Post
        fields = (
            "text_content",
            "location",
            "hashtags",
            "is_business_post",
            "is_personal_post",
            "tagged_users",
        )

    def create(self, validated_data):

        user = self.context["user"]

        post = self.context["post"]

        text_content = self.context["text_content"]

        if type(text_content) != str:
            raise BadRequestException("text content must be a string.")

        tagged_users_data = validated_data.pop("tagged_users", [])

        hashtags_data = validated_data.pop("hashtags", [])

        new_hashtags = [
            m.Hashtag.objects.get_or_create(name=name)[0].id for name in hashtags_data
        ]

        try:
            instance = m.Post.objects.create(
                user=user,
                is_repost=True,
                text_content=text_content,
                repost=post,
                **validated_data
            )
            instance.tagged_users.set(tagged_users_data)
            instance.hashtags.set(new_hashtags)

        except IntegrityError as e:

            raise BadRequestException(
                "One or more user IDs in the tagged users do not exist"
            )

        return instance
