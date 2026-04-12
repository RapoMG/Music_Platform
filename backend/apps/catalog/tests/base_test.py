from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from datetime import timedelta, date

from apps.catalog.models import Artist, Album, Song, Genre

class BaseTest(TestCase):
    def setUp(self):
        # Create a test artist
        self.artist = Artist.objects.create(
            name="Test Artist",
            description="Some description",
            image=SimpleUploadedFile("artist.jpg", b"file_content", content_type="image/jpeg")
        )

        # Create a test album
        self.album = Album.objects.create(
            artist=self.artist,
            title="Album 1",
            cover=SimpleUploadedFile("cover.jpg", b"file_content"),
            release_date=date.today()
        )

        # Create a test song
        self.song = Song.objects.create(
            album=self.album,
            title="Song 1",
            track_no=1,
            file=SimpleUploadedFile("song.mp3", b"file_content"),
            length=timedelta(minutes=3)
        )

        # Create another test song for the same album, but with a different track number
        Song.objects.create(
            album=self.album,
            title="Song 2",  # This title is a little blur
            track_no=2,
            file=SimpleUploadedFile("song2.mp3", b"file_content"),
            length=timedelta(minutes=4)
        )

        # Create a test genre
        self.genre = Genre.objects.create(name="Metal")
        self.album.genre.add(self.genre)