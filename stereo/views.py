from rest_framework import generics, status, viewsets, decorators
from rest_framework.response import Response

from . import models as m
from . import serializers as s

from .permissions import HasStereoAccountPermission
from rest_framework.permissions import AllowAny


class ArtistAPI(
    generics.ListAPIView, generics.RetrieveAPIView, viewsets.GenericViewSet
):
    serializer_class = s.ArtistSerializer

    def get_queryset(self):
        if self.action == "profile":
            return m.Artist.objects.filter(profile=self.request.user.profile)
        return m.Artist.objects.all()

    def get_permissions(self):
        if self.action == "profile":
            permissions = [HasStereoAccountPermission]
        else:
            permissions = [AllowAny]
        return [permission() for permission in permissions]

    @decorators.action(methods=["GET"], detail=False, url_path="profile")
    def profile(self, request, *args, **kwargs):
        data = s.ArtistSerializer(self.get_queryset().first()).data
        return Response(data, status=status.HTTP_200_OK)

    @decorators.action(methods=["GET"], detail=False, url_path="create-artist")
    def create_artist(self, request, *args, **kwargs):
        serializer = s.ArtistSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @decorators.action(methods=["GET"], detail=False, url_path="stick-artist")
    def stick(self, request, *args, **kwargs):
        pass


class SongAPI(generics.ListAPIView, generics.RetrieveAPIView, viewsets.GenericViewSet):
    serializer_class = s.SongSerializer

    def get_queryset(self):
        return m.Song.objects.all()

    @decorators.action(methods=["GET"], detail=False, url_path="categories")
    def categories(self, request, *args, **kwargs):
        song_categories = m.SongCategory.objects.all()
        data = s.SongCategorySerializer(song_categories, many=True).data
        return Response(data, status=status.HTTP_200_OK)

    @decorators.action(
        methods=["GET"], detail=False, url_path="categories/<str:category_id>"
    )
    def category_detail(self, request, *args, **kwargs):
        category_id = int(kwargs.get("category_id", 0))
        song_category = m.SongCategory.objects.filter(id=category_id)
        if song_category.exists():
            data = s.SongCategorySerializer(song_category.first()).data
            return Response(data, status=status.HTTP_200_OK)
        return Response({"detail": "Not Found"}, status=status.HTTP_404_NOT_FOUND)


class SongLibraryAPI(viewsets.GenericViewSet):
    serializer_class = s.SongLibrarySerializer

    def get_queryset(self):
        return m.Library.objects.filter(profile=self.request.user.profile)

    @decorators.action(methods=["GET"], detail=False, url_path="retrieve")
    def library(self, request, *args, **kwargs):
        data = s.SongLibrarySerializer(self.get_queryset().first()).data
        return Response(data, status=status.HTTP_200_OK)
