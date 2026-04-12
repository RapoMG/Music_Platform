from .base_test import BaseTest

from apps.catalog.serializers import (
    ArtistSerializer,
    AlbumSerializer,
    SongSerializer,
    GenreSerializer
)


class ArtistSerializerTest(BaseTest):

    def test_artist_serializer_output(self):
        serializer = ArtistSerializer(self.artist)
        data = serializer.data

        self.assertEqual(data["name"], "Test Artist", f"Artist name should be 'Test Artist', but is '{data['name']}'.")
        self.assertEqual(data["description"], "Some description", f"Description should be 'Some description', but is '{data['description']}'.")
        self.assertIn("albums", data, f"Albums should be in data, but are not.")


class GenreSerializerTest(BaseTest):

    def test_genere_serializer(self):
        #genre = Genre.objects.create(name="Rock")
        serializer = GenreSerializer(self.genre)

        self.assertEqual(serializer.data["name"], "Metal", f"Genre name should be 'Metal', but is '{serializer.data['name']}'.")


class AlbumSerializerTest(BaseTest):

    def test_album_nested_artist(self):
        serializer = AlbumSerializer(self.album)
        data = serializer.data

        self.assertEqual(data["artist"]["name"], "Test Artist", f"Artist name should be 'Test Artist', but is '{data['artist']['name']}'.")

    def test_album_genre_representation(self):
        serializer = AlbumSerializer(self.album)
        data = serializer.data

        self.assertIn("Metal", data["genre"], f"Genre name should be 'Metal', but is '{data['genre']}'.")


class SongSerializerTest(BaseTest):

    def test_song_serializer_fields(self):
        serializer = SongSerializer(self.song)
        data = serializer.data

        self.assertEqual(data["title"], "Song 1", f"Song title should be 'Song 1', but is '{data['title']}'.")
        self.assertEqual(data["track_no"], 1, f"Track number should be 1, but is '{data['track_no']}'.")
        self.assertEqual(data["album"], self.album.id, f"Album ID should be '{self.album.id}', but is '{data['album']}'.")