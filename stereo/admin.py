from django.contrib import admin

from . import models as m


@admin.register(m.SongCategory)
class SongCategoryAdmin(admin.ModelAdmin):
    list_display = ["name"]


@admin.register(m.Song)
class SongAdmin(admin.ModelAdmin):
    list_display = ["title"]


@admin.register(m.Album)
class AlbumAdmin(admin.ModelAdmin):
    list_display = ["name"]


@admin.register(m.Artist)
class ArtistAdmin(admin.ModelAdmin):
    list_display = ["full_name"]


@admin.register(m.Library)
class LibraryAdmin(admin.ModelAdmin):
    list_display = ["profile", "email"]

    def email(self, obj):
        return obj.profile.user.email


@admin.register(m.SearchSong)
class SearchSongAdmin(admin.ModelAdmin):
    list_display = ["keyword"]
