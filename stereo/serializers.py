from rest_framework import serializers

from . import models as m


class ArtistSerializer(serializers.ModelSerializer):
    class Meta:
        model = m.Artist
        field = "__all__"


class SongCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = m.SongCategory
        field = "__all__"


class SongSerializer(serializers.ModelSerializer):
    class Meta:
        model = m.Song
        field = "__all__"


class AlbumSerializer(serializers.ModelSerializer):
    class Meta:
        model = m.Album
        field = "__all__"
