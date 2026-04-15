from django.contrib import admin
from django.utils.html import format_html

from apps.catalog.models import Artist, Album, Song, Genre

# Register your models here.

class AlbumInline(admin.TabularInline):
    model = Album
    extra = 1

class SongInline(admin.TabularInline):
    model = Song
    extra = 1

class GenreInline(admin.TabularInline):
    model = Genre
    extra = 1


@admin.register(Artist)
class ArtistAdmin(admin.ModelAdmin):
    list_display = ('name', 'albums_no', 'songs_no', 'genres_names')

    inlines = [AlbumInline]

    @admin.display(description='Number of albums')
    def albums_no(self, obj):
        return obj.albums.count()
    
    @admin.display(description='Number of songs')
    def songs_no(self, obj):
        return Song.objects.filter(album__artist=obj).count()
    
    @admin.display(description='Genres')
    def genres_names(self, obj):
        names = Genre.objects.filter(genres__artist=obj).values_list('name', flat=True).distinct()
        return ', '.join(names) if names else '-'
    
@admin.register(Album)
class AlbumAdmin(admin.ModelAdmin):
    list_display = ('artist', 'title', 'songs_no', 'genres_names', 'release_date', 'published', 'cover_preview')
    list_filter = ('artist', 'genre', 'release_date', 'published')
    search_fields = ('title', 'artist__name',)

    ordering = ('artist','-release_date',)

    inlines = [SongInline, ]

    readonly_fields = ('artist','big_cover_preview',)

    fields = ('artist', 'title', 'cover', 'big_cover_preview', 'release_date', 'published', 'genre',)

    @admin.display(description='Number of songs')
    def songs_no(self, obj):
        return obj.songs.count()
    
    @admin.display(description='Genres')
    def genres_names(self, obj):
        names = obj.genre.values_list('name', flat=True)
        return ', '.join(names) if names else '-'
    
    @admin.display(description='Cover')
    def cover_preview(self, obj):
        if not obj.cover:
            return '-'
        try:
            return format_html('<img src="{}" style="height: 100px;" />', obj.cover.url)
        except ValueError:
            return '-'
        
    @admin.display(description='Cover')
    def big_cover_preview(self, obj):
        if not obj.cover:
            return '-'
        try:
            return format_html('<img src="{}" style="height: 450px;" />', obj.cover.url)
        except ValueError:
            return '-'
    
@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ('name',)
