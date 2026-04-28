from django.db import models

# Create your models here.

class Artist(models.Model):
    """Artist model. Related to Album model."""
    name = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to='media/artists/', null=True, blank=True)
    
    def __str__(self):
        return self.name

class Album(models.Model):
    """Album model. Related to: Artist model, Song model."""
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE, related_name='albums')
    
    title = models.CharField(max_length=100, default='Untitled')
    cover = models.ImageField(upload_to='albums/', default='albums/default.png')
    release_date = models.DateField()

    published = models.BooleanField(default=False)
    genre = models.ManyToManyField('Genre', blank=True, related_name='genres')

    def __str__(self):
        return self.title

class Song(models.Model):
    """Song model. Related to Album model."""
    album = models.ForeignKey(Album, on_delete=models.CASCADE, related_name='songs')
    
    title = models.CharField(max_length=100, default='Untitled')
    track_no = models.IntegerField(default=1)
    
    file = models.FileField(upload_to='songs/')
    length = models.DurationField()

    lyrics = models.TextField(null=True, blank=True)
    author = models.CharField(max_length=250, null=True, blank=True)

    def __str__(self):
        return self.title
    
    class Meta:
        unique_together = ('album', 'track_no')
        ordering = ['track_no']

class Genre(models.Model):
    """Genre model. Related to Album model."""
    name = models.CharField(max_length=50, unique=True)
    
    def __str__(self):
        return self.name
