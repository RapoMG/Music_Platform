from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager

from .validators import validate_username_not_email

# Create your models here.

class UserManager(BaseUserManager):
    """
    Custom user manager.
    """
    def normalize_email(self, email):
        email = super().normalize_email(email)
        return email.lower() if email else email
    
    def create_user(self, username, email, password=None, **kwargs):
        if not email:
            raise ValueError('Email is required.')
        
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **kwargs)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, username, email, password=None, **kwargs):
        kwargs.setdefault('is_staff', True)
        kwargs.setdefault('is_superuser', True)
        return self.create_user(username, email, password, **kwargs)
    

class User(AbstractUser):
    """
    Custom user model.
    Username cannot be an email.
    """
    ACCOUNT_TYPE_CHOICES = (
        ('consumer', 'Consumer'),
        ('creator', 'Creator'),
    )
    # username = AbstractUser._meta.get_field('username').clone()
    # username.validators.append(validate_username_not_email)

    objects = UserManager()

    username = models.CharField(max_length=150, unique=True, validators=[validate_username_not_email])
    email = models.EmailField(max_length=255, unique=True)

    account_type = models.CharField(max_length=10, choices=ACCOUNT_TYPE_CHOICES, default='consumer')


    def __str__(self):
        return self.username
    
