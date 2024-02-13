from django.db import models
from django.utils.translation import gettext as _

from user.models import UserProfile

# class StereoAccount(models.Model):
#     profile = models.OneToOneField(
#         to=UserProfile,
#         on_delete=models.CASCADE,
#         verbose_name=_("User Profile"),
#         related_name="stereo_account",
#     )
#     created_at = models.DateTimeField(auto_now_add=True)

#     def __str__(self) -> str:
#         return self.profile.user.email


class Library(models.Model):
    profile = models.OneToOneField(
        to=UserProfile, on_delete=models.CASCADE, verbose_name=_("User Profile")
    )


class Artist(models.Model):
    profile = models.OneToOneField(
        to=UserProfile, on_delete=models.CASCADE, verbose_name=_("User Profile")
    )
    artist_name = models.CharField(
        _("Artist Name"), max_length=50, blank=True, null=True
    )
    about = models.TextField(_("About"), blank=True, null=True)
    picture = models.ImageField(_("Picture"), blank=True, null=True)
    stickers = models.PositiveIntegerField(_("Stickers"), default=0)
    # library = models.ForeignKey(to=Library, verbose_name=_("Library"))
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.artist_name


class SongCategory(models.Model):
    name = models.CharField(_("Category Name"), max_length=100)
    description = models.CharField(_("Description"), max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "SongCategories"

    def __str__(self) -> str:
        return self.name


class SongManager(models.Manager):
    """Model manager for Song model"""

    def search(self, query):
        pass

    def recent_uploads(self):
        pass


class Song(models.Model):
    title = models.CharField(_("Song Title"), max_length=100)
    artist = models.ForeignKey(
        to=Artist,
        on_delete=models.SET_NULL,
        verbose_name=_("Artist"),
        blank=True,
        null=True,
    )
    duration = models.CharField(_("Duration"), max_length=20, blank=True, null=True)
    category = models.ManyToManyField(to=SongCategory, verbose_name=_("Category"))
    cover_image = models.ImageField(
        _("Cover Image"), upload_to="song-cover-images", blank=True, null=True
    )
    audio_file = models.FileField(
        _("Song File"), upload_to="songs", blank=True, null=True
    )
    likes = models.ManyToManyField(
        to=UserProfile, verbose_name=_("Downloads"), blank=True, null=True
    )
    downloads = models.ManyToManyField(
        to=UserProfile, verbose_name=_("Downloads"), blank=True, null=True
    )
    plays = models.ManyToManyField(
        to=UserProfile, verbose_name=_("Plays"), blank=True, null=True
    )
    stickers = models.ManyToManyField(
        to=UserProfile, verbose_name=_("Stickers"), blank=True, null=True
    )
    download_count = models.PositiveIntegerField(_("Download Count"), default=0)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    objects = SongManager()

    def __str__(self) -> str:
        return self.title

    @property
    def likes(self):
        # getter for likes attribute
        return 10  # placeholder

    @property
    def downloads(self):
        # getter for downloads attr
        return 10

    @property
    def plays(self):
        # getter for plays attr
        return 10

    @property
    def stickers(self):
        # getter for stickers attr
        return 10


class Playlist(models.Model):
    name = models.CharField(_("Name"), max_length=100)
    description = models.CharField(
        _("Description"), max_length=1000, blank=True, null=True
    )
    library = models.ForeignKey(
        to=Library,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        verbose_name=_("Library"),
    )
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
    library = models.ForeignKey(
        to=Library,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        verbose_name=_("Library"),
    )
    cover_image = models.ImageField(
        _("Cover Image"), upload_to="album-cover-images", blank=True, null=True
    )
    songs = models.ManyToManyField(to=Song, verbose_name=_("Songs"))
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.name


class SearchSong(models.Model):
    keyword = models.CharField(_("Search Keyword"), max_length=100)
    profile = models.ForeignKey(
        to=UserProfile, on_delete=models.CASCADE, blank=True, null=True
    )
    searched_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "SearchSong"
        verbose_name_plural = "SearchSongs"

    def __str__(self) -> str:
        return self.keyword
