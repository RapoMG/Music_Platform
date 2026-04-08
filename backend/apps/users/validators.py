from django.core.validators import validate_email
from django.core.exceptions import ValidationError

    
def validate_username_not_email(username):
    """
    Check if the username is not an email.
    """
    try:
        validate_email(username)

    # if username is not a valid email (correct format)
    except ValidationError:
        return

    # if username is a valid email
    raise ValidationError('Username cannot be an email.')
    
