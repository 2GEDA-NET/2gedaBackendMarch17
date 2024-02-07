from django.db import models
from django.utils.translation import gettext as _

from user.models import UserProfile


class Library(models.Model):
    profile = models.OneToOneField(to=UserProfile, verbose_name=_("User Profile"))


class Artist(models.Artist):
    full_name = models.CharField(_("Name"))
    about = models.TextField(_("About"), blank=True, null=True)
    picture = models.ImageField(_("Picture"), blank=True, null=True)
    stickers = models.PositiveIntegerField(_("Stickers"), default=0)
    # library = models.ForeignKey(to=Library, verbose_name=_("Library"))
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.title


class SongCategory(models.Model):
    name = models.CharField(_("Category Name"), max_length=100)
    description = models.CharField(_("Description"), max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_plural_name = "SongCategories"

    def __str__(self) -> str:
        return self.name


class Song(models.Model):
    title = models.CharField(_("Song Title"), max_length=100)
    artist = models.ForeignKey(
        to=Artist, verbose_name=_("Artist"), blank=True, null=True
    )
    duration = models.CharField(_("Duration"), max_length=20, blank=True, null=True)
    category = models.ManyToManyField(
        to=SongCategory, verbose_name=_("Category"), blank=True, null=True
    )
    likes = models.PositiveIntegerField(_("Likes"), default=0)
    cover_image = models.ImageField(
        _("Cover Image"), upload_to="song-cover-images", blank=True, null=True
    )
    song_file = models.FileField(
        _("Song File"), upload_to="songs", blank=True, null=True
    )
    is_downloaded = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.title


class Playlist(models.Model):
    name = models.CharField(_("Name"), max_length=100)
    description = models.CharField(
        _("Description"), max_length=1000, blank=True, null=True
    )
    library = models.ForeignKey(to=Library, verbose_name=_("Library"))
    cover_image = models.ImageField(
        _("Cover Image"), upload_to="playlist-cover-images", blank=True, null=True
    )
    songs = models.ManyToManyField(to=Song, verbose_name=_("Songs"))
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.name

    @property
    def total_duration(self):
        pass

    @property
    def total_songs(self):
        pass


class Album(models.Model):
    name = models.CharField(_("Name"), max_length=100)
    about = models.TextField(_("About"), blank=True, null=True)
    artist = models.ForeignKey(
        to=Artist, on_delete=models.SET_NULL, blank=True, null=True
    )
    library = models.ForeignKey(to=Library, verbose_name=_("Library"))
    cover_image = models.ImageField(
        _("Cover Image"), upload_to="album-cover-images", blank=True, null=True
    )
    songs = models.ManyToManyField(to=Song, verbose_name=_("Songs"))
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.name
