from django.core.management.base import BaseCommand

from faker import Faker

fake = Faker('en_US')


# def fetch_cover():
#     url = "https://picsum.photos/300/300"
#     response = requests.get(url)
#     return ContentFile(response.content, name="cover.jpg")

import requests
from django.core.files.base import ContentFile
from uuid import uuid4

for i in range(10):
    print(f'{i}: fake.name()')

def fetch_random_album_cover():
    """
    Fetch random image from Picsum and return Django-compatible file.
    """
    url = "https://picsum.photos/300/300"

    response = requests.get(url)
    response.raise_for_status()

    file_name = f"album_{uuid4().hex}.jpg"

    return ContentFile(response.content, name=file_name)

if response.raise_for_status():
    return ContentFile(name='default.png')