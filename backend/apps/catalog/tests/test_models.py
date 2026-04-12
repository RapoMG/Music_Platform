from .base_test import BaseTest

# For duplicate creation tests 
from django.core.files.uploadedfile import SimpleUploadedFile
from datetime import timedelta

from apps.catalog.models import Song, Genre



class ArtistModelTest(BaseTest):

    def test_artist_str_representation(self):
        # Test that the string representation of the artist is correct
        self.assertEqual(str(self.artist), "Test Artist", f"Artist name should be 'Test Artist', but is '{str(self.artist)}'.")

        # Test that the description field is set
        self.assertEqual(self.artist.description, "Some description", f"Description should be 'Some description', but is '{self.artist.description}'.")
    
    def test_artist_image_field(self):
        # Test that the image field is set
        self.assertIsNotNone(self.artist.image, f"Image should not be None.")


class AlbumModelTest(BaseTest):

    def test_album_str_representation(self):
        self.assertEqual(str(self.album), "Album 1", f"Album name should be 'Album 1', but is '{str(self.album)}'.")

    def test_album_artist_relation(self):
        self.assertEqual(self.album.artist, self.artist, f"Album artist should be {self.artist}, but is {self.album.artist}.")
        self.assertIn(self.album, self.artist.albums.all(), f"Album {self.album} should be in {self.artist.albums.all()}")


class SongModelTest(BaseTest):

    def test_song_str_representation(self):
        self.assertEqual(str(self.song), "Song 1", f"Song name should be 'Song 1', but is '{str(self.song)}'.")

    def test_song_ordering(self):
        # Test that the songs are ordered by track number
        songs = self.album.songs.all()
        self.assertEqual(songs[0].track_no, 1, f"First song should have track number 1, but has {songs[0].track_no}")
        self.assertEqual(songs[1].track_no, 2, f"Second song should have track number 2, but has {songs[1].track_no}")

    def test_song_unique_track_per_album(self):
        # Test that a song with the same track number cannot be created
        with self.assertRaises(Exception, msg="Song with the same track number already exists"):
            Song.objects.create(
                album=self.album,
                title="Duplicate Track",
                track_no=1,  # same track_no → should fail
                file=SimpleUploadedFile("dup.mp3", b"file_content"),
                length=timedelta(minutes=3)
            )


class GenreModelTest(BaseTest):

    def test_genere_unique_name(self):
        with self.assertRaises(Exception, msg="Genre name should be unique"):
            Genre.objects.create(name="Metal")

    def test_genere_str_representation(self):
        self.assertEqual(str(self.genre), "Metal", f"Genre name should be 'Metal', but is '{str(self.genre)}'.")