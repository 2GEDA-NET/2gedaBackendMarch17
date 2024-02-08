from rest_framework import generics, status, viewsets
from rest_framework.response import Response

from . import models as m
from . import serializers as s


class ArtistAPI(viewsets.ModelViewSet):
    serializer_class = s.ArtistSerializer

    def get_queryset(self):
        return m.Artist.objects.filter(library=self.request.user.profile.library)
