from django.db import migrations, models


def forwards_fix_song_paths(apps, schema_editor):
    Song = apps.get_model("catalog", "Song")
    for song in Song.objects.filter(file__startswith="media/songs/").iterator():
        song.file.name = song.file.name.removeprefix("media/")
        song.save(update_fields=["file"])


def backwards_fix_song_paths(apps, schema_editor):
    Song = apps.get_model("catalog", "Song")
    for song in Song.objects.filter(file__startswith="songs/").iterator():
        song.file.name = f"media/{song.file.name}"
        song.save(update_fields=["file"])


class Migration(migrations.Migration):

    dependencies = [
        ("catalog", "0004_fix_album_cover_default_path"),
    ]

    operations = [
        migrations.AlterField(
            model_name="song",
            name="file",
            field=models.FileField(upload_to="songs/"),
        ),
        migrations.RunPython(forwards_fix_song_paths, backwards_fix_song_paths),
    ]
