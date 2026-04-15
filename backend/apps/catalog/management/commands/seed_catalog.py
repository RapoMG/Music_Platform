from django.core.management.base import BaseCommand
from django.core.files.base import ContentFile
from django.core.files.uploadedfile import SimpleUploadedFile


from faker import Faker
import requests
from uuid import uuid4
from random import randint, sample
from datetime import timedelta

from apps.catalog.models import Genre, Artist, Album, Song


def fetch_random_album_cover():
    """
    Fetch random image from Picsum and return Django-compatible file.
    """
    url = "https://picsum.photos/300/300"

    try:
        response = requests.get(url, timeout=3)
        response.raise_for_status()

        file_name = f"album_{uuid4().hex}.jpg"

        return ContentFile(response.content, name=file_name)
    except requests.RequestException:
        return None


class Command(BaseCommand):
    help = '''Seed the database with fake data generated from Faker library.\n
    Artist will have albums, albums will have songs and genres.\n
    Artist: name is 2-3 words separated by space, description is paragraph of 9-11 sentences separated by new line. 
    Album: title is 2-3 words separated by space, cover is random image from Picsum, release date is random.
    Song: title is 2-3 words separated by space, tracks are numbered from 1 to max number of songs, length is random in range 1-5:59 minutes.
    Genres: names are randomly selected (6 by default) from predefined list. Albums can have 1-3 genres from this set.

    Before seeding data, user will be asked if old data should be removed if it exists.
    '''

    def add_arguments(self, parser):
        """
        Add arguments to the command.
        """
        parser.add_argument('--artists', type=int, default=5, help='Number of artists to create (default=5)')
        parser.add_argument('--albums', type=int, default=3, help='Number of albums to create (default=3)')
        parser.add_argument('--songs', type=int, default=10, help='Number of songs to create (default=10)')
        parser.add_argument('--genres', type=int, default=6, help='Number of genres to create (default=6)')

    def handle(self, *args, **options):
        # Number of created objects
        art_no = options['artists']
        alb_no = options['albums']
        song_no = options['songs']
        gen_no = options['genres']

        # Prepare to remove old data
        if not self.remove_data():
            abort = input('Abort creation? [Y/N] ')
            if abort.lower().strip() == 'y':
                self.stdout.write(self.style.NOTICE('Creation aborted.\n'))
                return

        # Predefined genres
        pre_genres = ['Blues','Country','Classical','Dance','Electronic','Folk','Funk','HipHop','Jazz','Pop','Punk','Regae','Rock','Metal',]

        # Removing existing genres from the list
        ex = Genre.objects.values_list('name', flat=True)
        pre_genres = list(set(pre_genres) - set(ex))

        # Limit number of genres
        if gen_no > len(pre_genres):
            self.stdout.write(self.style.NOTICE(f'Number of genres is limited to {len(pre_genres)}'))
            gen_no = len(pre_genres)


        self.stdout.write(self.style.SUCCESS('Creating fake data...'))
        
        fake = Faker('en_US')

        # Genres 
        # Random genres from pre_genres list, repeated gen_no times
        genres = [Genre.objects.create(name=gen) for gen in sample(pre_genres, gen_no)]
        

        # Artists
        artists = []
        for _ in range(art_no):
            # Fake Band name
            name = fake.sentence(randint(1,4))
            name = name.title().replace(".", "")
            
            artists.append(Artist.objects.create(name=name, description=fake.paragraph(10, True)))

        # Albums
        albums = 0
        songs = 0
        for artist in artists:
            for _ in range(alb_no):
                album = Album.objects.create(
                    artist=artist,
                    title=fake.sentence(randint(1,4)).title().replace(".", ""),
                    cover=fetch_random_album_cover(),
                    release_date=fake.date_object(),
                    published=True,
                )
                album.genre.set(sample(genres, randint(1, 3)))
                cover = fetch_random_album_cover()
                if cover:
                    album.cover.save(cover.name, cover, save=True)
                albums += 1

                # Songs
                for track in range(song_no):
                    song = Song.objects.create(
                        album=album,
                        title=fake.sentence(randint(1,4)).title().replace(".", ""),
                        track_no=track+1,
                        length=timedelta(minutes=randint(1,5), seconds=randint(0,59)),
                        lyrics=fake.paragraph(),
                    )
                    song_name = f"track_{track+1}_{uuid4().hex}.mp3"
                    song.file.save(song_name, SimpleUploadedFile(song_name, b"file_content"), save=True)
                    songs += 1

        
        # Summary
        print('-'*15)
        self.stdout.write(self.style.SUCCESS(f'{len(genres)} genres created.'))
        self.stdout.write(self.style.SUCCESS(f'{len(artists)} artists created.'))
        self.stdout.write(self.style.SUCCESS(f'{albums} albums created.'))
        self.stdout.write(self.style.SUCCESS(f'{songs} songs created.'))
        print('-'*15)
        
        self.stdout.write(self.style.SUCCESS('Fake data created!'))

    def remove_data(self) -> bool:
        """
        Remove all genres, artists, albums and songs. Returns True if data was removed.
        """
        genres = Genre.objects.all()
        artists = Artist.objects.all()
        albums = Album.objects.all()
        songs = Song.objects.all()

        # single or plural
        genres_msg = f'{len(genres)} {"genre" if len(genres) == 1 else "genres"}'
        artists_msg = f'{len(artists)} {"artist" if len(artists) == 1 else "artists"}'
        albums_msg = f'{len(albums)} {"album" if len(albums) == 1 else "albums"}'
        songs_msg = f'{len(songs)} {"song" if len(songs) == 1 else "songs"}'


        total = len(genres) + len(artists) + len(albums) + len(songs)

        if total > 0:
            self.stdout.write(self.style.NOTICE(f'There are {artists_msg} holding {albums_msg} in {genres_msg} with {songs_msg} total.'))
            self.stdout.write(self.style.WARNING('Delete it before creating new ones? [Y/N]'))
            answ = input()
            if answ.lower().strip() == 'y':
                genres.delete()
                artists.delete()
                albums.delete()
                songs.delete()
                self.stdout.write(self.style.SUCCESS('Old data removed.'))
                return True
            else:
                self.stdout.write(self.style.NOTICE('Data not removed.'))
                return False
            
        self.stdout.write(self.style.NOTICE('No genres, artists, albums or songs in database.'))
        return True
    