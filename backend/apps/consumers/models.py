from django.db import models
from django.conf import settings

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