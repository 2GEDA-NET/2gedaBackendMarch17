from rest_framework import serializers

from . import models as m


class SongLibrarySerializer(serializers.ModelSerializer):
    class Meta:
        model = m.Library
        fields = "__all__"


class ArtistSerializer(serializers.ModelSerializer):
    class Meta:
        model = m.Artist
        fields = "__all__"


class SongCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = m.SongCategory
        fields = "__all__"


class SongSerializer(serializers.ModelSerializer):
    class Meta:
        model = m.Song
        fields = "__all__"


class AlbumSerializer(serializers.ModelSerializer):
    class Meta:
        model = m.Album
        fields = "__all__"
