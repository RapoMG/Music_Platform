from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from django import forms

from apps.consumers.models import ConsumerProfile, Playlist

User = get_user_model()

class CustomUserCreationForm(UserCreationForm):
    # password fields are at this level within parent class
    class Meta(UserCreationForm.Meta):  # Inherits from UserCreationForm.Meta not replaces as Meta(), so it keeps other properties like help_texts.
        model = User
        fields = ("username", "email")

# Code stube for future use when we want to have custom login form, but for now we can use default one with custom backend
# class CustomAuthenticationForm(forms.Form):
#     username = forms.CharField()
#     password = forms.CharField(widget=forms.PasswordInput)


class ProfileForm(forms.ModelForm):
    class Meta:
        model = ConsumerProfile  # Access the related Profile model through the User model
        fields = ['avatar', 'description']

class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['email']

class PlaylistForm(forms.ModelForm):
    class Meta:
        model = Playlist
        fields = ['name', 'is_public', 'description']
        