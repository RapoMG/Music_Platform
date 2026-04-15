from django.db import migrations


def forwards_fix_cover_paths(apps, schema_editor):
    Album = apps.get_model("catalog", "Album")
    Album.objects.filter(cover="default.png").update(cover="albums/default.png")


def backwards_fix_cover_paths(apps, schema_editor):
    Album = apps.get_model("catalog", "Album")
    Album.objects.filter(cover="albums/default.png").update(cover="default.png")


class Migration(migrations.Migration):

    dependencies = [
        ("catalog", "0003_alter_album_cover"),
    ]

    operations = [
        migrations.RunPython(forwards_fix_cover_paths, backwards_fix_cover_paths),
    ]

