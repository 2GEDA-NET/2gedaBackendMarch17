from rest_framework import serializers

from .models import *


class PostMediaSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostMedia
        fields = "__all__"


class ReactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reaction
        fields = ["reaction_type"]


class CommentSerializer(serializers.ModelSerializer):
    reaction = ReactionSerializer()

    class Meta:
        model = Comment
        fields = "__all__"


class ReplySerializer(serializers.ModelSerializer):
    reaction = ReactionSerializer()

    class Meta:
        model = Reply
        fields = "__all__"


class PostSerializer(serializers.ModelSerializer):
    reaction = ReactionSerializer()
    media = PostMediaSerializer(required=False)  # Nested serializer for media upload
    comments = CommentSerializer(many=True)

    class Meta:
        model = Post
        fields = "__all__"

    def create(self, validated_data):
        media_data = validated_data.pop("media", None)
        post = Post.objects.create(**validated_data)

        if media_data:
            PostMedia.objects.create(post=post, **media_data)

        return post


class RepostSerializer(serializers.ModelSerializer):
    reaction = ReactionSerializer()
    comments = CommentSerializer(many=True)

    class Meta:
        model = Repost
        fields = "__all__"


class SavedPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = SavedPost
        fields = "__all__"


class PromotedPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = PromotedPost
        fields = "__all__"


# class PostMediaSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = PostMedia
#         fields = ('image', )


# Define document file extensions

video_extensions = [
    ".mp4",
    ".avi",
    ".mkv",
    ".mov",
    ".wmv",
    ".flv",
    ".webm",
    ".ogg",
    ".3gp",
    ".mpeg",
    ".vob",
    ".divx",
    ".rm",
    ".m4v",
    ".ts",
    ".m2ts",
    ".ogv",
    ".asf",
    ".mpg",
    ".mp2",
    ".m2v",
    ".mxf",
    ".mts",
    ".m2t",
    ".m1v",
    ".mpv",
]


class VideoPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = "__all__"

    def to_representation(self, instance):
        # Serialize only if the associated file has a video extension
        if instance.file and any(
            instance.file.media.name.endswith(ext) for ext in video_extensions
        ):
            return super().to_representation(instance)
        return None


# Define document file extensions
document_extensions = [".pdf", ".doc", ".docx", ".txt", ".rtf"]


class DocumentPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = "__all__"

    def to_representation(self, instance):
        # Serialize only if the associated file has a document extension
        if instance.file and any(
            instance.file.media.name.endswith(ext) for ext in document_extensions
        ):
            return super().to_representation(instance)
        return None


# Define audio file extensions
audio_extensions = [
    ".mp3",
    ".wav",
    ".ogg",
    ".aac",
    ".flac",
    ".wma",
    ".m4a",
    ".opus",
    ".amr",
    ".mid",
    ".midi",
    ".ac3",
]


class AudioPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = "__all__"

    def to_representation(self, instance):
        # Serialize only if the associated file has an audio extension
        if instance.file and any(
            instance.file.media.name.endswith(ext) for ext in audio_extensions
        ):
            return super().to_representation(instance)
        return None


image_extensions = [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".tiff", ".webp"]


class ImagePostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = "__all__"

    def to_representation(self, instance):
        # Serialize only if the associated file has an image extension
        if instance.file and any(
            instance.file.media.name.endswith(ext) for ext in image_extensions
        ):
            return super().to_representation(instance)
        return None


others_extensions = [
    ".exe",
    ".msi",
    ".pkg",
    ".deb",
    ".rpm",
    ".dmg",
    ".zip",
    ".app",
    ".apk",
    ".jar",
    ".rar",
    ".7z",
    ".tar.gz",
    ".tgz",
    ".tar.bz2",
    ".tbz2",
    ".tar",
    ".cab",
    ".sit",
    ".sitx",
    ".zipx",
    ".z",
    ".lzh",
    ".lha",
    ".ace",
    ".arj",
    ".gz",
    ".bz2",
    ".xz",
    ".zst",
]


class OtherPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = "__all__"

    def to_representation(self, instance):
        # Serialize only if the associated file has an image extension
        if instance.file and any(
            instance.file.media.name.endswith(ext) for ext in others_extensions
        ):
            return super().to_representation(instance)
        return None
