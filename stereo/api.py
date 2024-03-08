from rest_framework import decorators, generics, status, viewsets
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from utils import renderers

from . import models as m
from . import serializers as s
from .permissions import HasStereoAccountPermission


class ArtistAPI(renderers.ReadOnlyModelRenderer, viewsets.GenericViewSet):
    serializer_class = s.ArtistSerializer
    lookup_url_kwarg = "artist_id"

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
        data = {"message": "Success", "status": True, "data": data}
        return Response(data, status=status.HTTP_200_OK)

    @decorators.action(methods=["POST"], detail=False, url_path="register")
    def create_artist(self, request, *args, **kwargs):
        serializer = s.ArtistSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        data = {"message": "Created", "status": True, "data": serializer.data}
        return Response(data, status=status.HTTP_201_CREATED)

    @decorators.action(methods=["GET"], detail=True, url_path="stick")
    def stick(self, request, *args, **kwargs):
        artist_id = kwargs.get("artist_id", 0)
        artist = m.Artist.objects.filter(pk=int(artist_id))
        if artist.exists():
            artist = artist.first()
            artist.profile.stickers.add(request.user.profile)
            return Response(
                {"message": f"You stick {artist.artist_name}!", "status": True}
            )
        return Response(
            {"message": "Invalid artist!", "status": False},
            status=status.HTTP_400_BAD_REQUEST,
        )

    @decorators.action(methods=["GET"], detail=True, url_path="unstick")
    def unstick(self, request, *args, **kwargs):
        artist_id = kwargs.get("artist_id", 0)
        artist = m.Artist.objects.filter(pk=int(artist_id))
        if artist.exists():
            artist = artist.first()
            artist.profile.stickers.remove(request.user.profile)
            return Response(
                {"message": f"You unstick {artist.artist_name}!", "status": True}
            )
        return Response(
            {"message": "Invalid artist!", "status": False},
            status=status.HTTP_400_BAD_REQUEST,
        )


class AlbumAPI(renderers.CrudModelRenderer, viewsets.GenericViewSet):
    # TODO coming back to add more action methods such as top-album, recent-album...
    serializer_class = s.AlbumSerializer
    queryset = m.Album.objects.all()
    lookup_url_kwarg = "album_id"

    @decorators.action(methods=["GET"], detail=False, url_path="top-album")
    def top_album(self, request, *args, **kwargs):
        albums = self.queryset.order_by("-created_at")
        data = self.serializer_class(albums, many=True).data
        return Response(
            {"message": "Success", "status": True, "data": data},
            status=status.HTTP_200_OK,
        )

    @decorators.action(methods=["GET"], detail=False, url_path="recent-album")
    def recent_album(self, request, *args, **kwargs):
        albums = self.queryset.order_by("-created_at")
        data = self.serializer_class(albums, many=True).data
        return Response(
            {"message": "Success", "status": True, "data": data},
            status=status.HTTP_200_OK,
        )


class SongAPI(renderers.CrudModelRenderer, viewsets.GenericViewSet):
    serializer_class = s.SongSerializer
    lookup_url_kwarg = "song_id"

    def get_queryset(self):
        return m.Song.objects.all()

    def get_permissions(self):
        return [AllowAny()]

    @decorators.action(methods=["GET"], detail=False, url_path="categories")
    def categories(self, request, *args, **kwargs):
        song_categories = m.SongCategory.objects.all()
        data = s.SongCategorySerializer(song_categories, many=True).data
        data = {"message": "Success", "status": True, "data": data}
        return Response(data, status=status.HTTP_200_OK)

    @decorators.action(
        methods=["GET"], detail=False, url_path="categories/<category_id>"
    )
    def category_detail(self, request, *args, **kwargs):
        category_id = int(kwargs.get("category_id", 0))
        song_category = m.SongCategory.objects.filter(id=category_id)
        if song_category.exists():
            data = s.SongCategorySerializer(song_category.first()).data
            data = {"message": "Success", "status": True, "data": data}
            return Response(data, status=status.HTTP_200_OK)
        return Response(
            {"message": "Not Found", "status": False}, status=status.HTTP_404_NOT_FOUND
        )

    @decorators.action(methods=["GET"], detail=True, url_path="download")
    def download(self, request, *args, **kwargs):
        song_id = kwargs.get("song_id", 0)
        songs = m.Song.objects.filter(pk=int(song_id))
        if songs.exists():
            song = songs.first()
            song.downloads.add(request.user.profile)
            return Response(
                {
                    "message": "Download",
                    "status": True,
                    "data": s.SongSerializer(song).data,
                },
                status=status.HTTP_200_OK,
            )
        return Response(
            {"message": "Invalid song id.", "status": False}, status=status.HTTP_200_OK
        )

    @decorators.action(methods=["GET"], detail=True, url_path="play")
    def play(self, request, *args, **kwargs):
        song_id = kwargs.get("song_id", 0)
        songs = m.Song.objects.filter(pk=int(song_id))
        if songs.exists():
            song = songs.first()
            song.plays.add(request.user.profile)
            return Response(
                {
                    "message": "Play",
                    "status": True,
                    "data": s.SongSerializer(song).data,
                },
                status=status.HTTP_200_OK,
            )
        return Response(
            {"message": "Invalid song id.", "status": False}, status=status.HTTP_200_OK
        )

    @decorators.action(methods=["GET"], detail=True, url_path="like")
    def like(self, request, *args, **kwargs):
        song_id = kwargs.get("song_id", 0)
        songs = m.Song.objects.filter(pk=int(song_id))
        if songs.exists():
            song = songs.first()
            song.likes.add(request.user.profile)
            return Response(
                {
                    "message": "Like",
                    "status": True,
                    "data": s.SongSerializer(song).data,
                },
                status=status.HTTP_200_OK,
            )
        return Response(
            {"message": "Invalid song id.", "status": False}, status=status.HTTP_200_OK
        )

    @decorators.action(methods=["GET"], detail=False, url_path="trending")
    def trending(self, request, *args, **kwargs):
        songs = self.get_queryset().order_by("-uploaded_at")
        data = self.serializer_class(songs, many=True).data
        return Response(
            {"message": "Success", "status": True, "data": data},
            status=status.HTTP_200_OK,
        )

    @decorators.action(methods=["GET"], detail=False, url_path="recent_upload")
    def recent_upload(self, request, *args, **kwargs):
        songs = self.get_queryset().order_by("-uploaded_at")
        data = self.serializer_class(songs, many=True).data
        return Response(
            {"message": "Success", "status": True, "data": data},
            status=status.HTTP_200_OK,
        )


class SongLibraryAPI(viewsets.GenericViewSet):
    serializer_class = s.SongLibrarySerializer

    def get_queryset(self):
        return m.Library.objects.filter(profile=self.request.user.profile)

    @decorators.action(methods=["GET"], detail=False, url_path="retrieve")
    def library(self, request, *args, **kwargs):
        data = s.SongLibrarySerializer(self.get_queryset().first()).data
        data = {"message": "Success", "status": True, "data": data}
        return Response(data, status=status.HTTP_200_OK)
