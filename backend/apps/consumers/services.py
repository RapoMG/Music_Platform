from apps.users.models import User
from apps.consumers.models import ConsumerProfile

def create_consumer_user(data):
    user = User.objects.create_user(
        username=data["username"],
        email=data["email"],
        password=data["password"],
        account_type="consumer"
    )

    ConsumerProfile.objects.create(user=user)
    return user