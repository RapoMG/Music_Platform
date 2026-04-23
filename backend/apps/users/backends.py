from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from django.core.validators import validate_email
from django.core.exceptions import ValidationError

User = get_user_model()

class UsernameOrEmailAccountTypeBackend(ModelBackend):
    """
    Allows the user to log in using either username or email using the same field in the login form.
    """
    def authenticate(self, request, username=None, password=None, account_type=None, **kwargs):
        user = None

        # Check if input is email
        try:
            validate_email(username)
            user = User.objects.filter(email__iexact=username).first()
        except ValidationError:
            user = User.objects.filter(username__iexact=username).first()

        if not user:
            return None

        if account_type and user.account_type != account_type:
            return None
        
        if not self.user_can_authenticate(user):
            return None

        if user and user.check_password(password):
            return user

        return None


# class UsernameEmailAccountTypeBackend(ModelBackend):
#     def authenticate(self, request, username=None, password=None, account_type=None, **kwargs):
#         user = None

#         if "@" in username:
#             user = User.objects.filter(email__iexact=username).first()
#         else:
#             user = User.objects.filter(username__iexact=username).first()

#         if not user:
#             return None

#         if account_type and user.account_type != account_type:
#             return None

#         if user.check_password(password):
#             return user

#         return None