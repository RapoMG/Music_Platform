from django.db import models
from django.conf import settings
from apps.catalog.models import Song

# Create your models here.

User = settings.AUTH_USER_MODEL

class ConsumerProfile(models.Model):
    """
    Profile model.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(default='default.jpg', upload_to='profile_pics')
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.user.username} ConsumerProfile'
    

class LibraryItem(models.Model):
    """
    Represents ownership of a song by a user.
    This is the user's "Library".
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='library_items')  #relates to Consumer
    song = models.ForeignKey(Song, on_delete=models.CASCADE, related_name='owned_by')  #relates to  purchased Song
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'song')
        ordering = ['-added_at']

    def __str__(self):
        return f"{self.user} owns {self.song}"
