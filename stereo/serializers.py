from rest_framework import serializers

from . import models as m
from account.serializers import UserProfileSerializer
from account.models import UserProfile


class SongLibrarySerializer(serializers.ModelSerializer):
    class Meta:
        model = m.Library
        fields = "__all__"


class SongCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = m.SongCategory
        fields = "__all__"

    def to_representation(self, instance):
        return super().to_representation(instance)


class WriteOnlySongSerializer(serializers.Serializer):
    title = serializers.CharField()
    category = SongCategorySerializer()
    song_file = serializers.FileField()


class ArtistSerializer(serializers.ModelSerializer):
    # profile = UserProfileSerializer(read_only=True)

    class Meta:
        model = m.Artist
        fields = "__all__"

    # def to_representation(self, instance):
    #     data = super().to_representation(instance)
    #     profile = UserProfile.objects.filter()
    #     return data


class MinimalArtistSerializer(serializers.ModelSerializer):
    class Meta:
        model = m.Artist
        exclude = ["profile", "created_at", "updated_at"]

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data["profile_picture"] = instance.profile.profile_image
        return data


class SongSerializer(serializers.ModelSerializer):
    # artist = MinimalArtistSerializer(read_only=True)
    categories = serializers.SerializerMethodField()

    class Meta:
        model = m.Song
        fields = "__all__"
        read_only_fields = ["downloads", "plays", "likes", "category", "artist"]

    def get_categories(self, instance):
        categories = m.SongCategory.objects.filter()
        return SongCategorySerializer(categories, many=True).data

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data["likes"] = instance.likes.count()
        data["plays"] = instance.plays.count()
        data["downloads"] = instance.downloads.count()
        # data["duration"] = instance.duration.count()
        return data


class AlbumSerializer(serializers.ModelSerializer):
    songs = serializers.ListField(child=WriteOnlySongSerializer())

    class Meta:
        model = m.Album
        fields = ["name", "about", "songs"]
