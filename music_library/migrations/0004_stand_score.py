# Generated by Django 3.0.9 on 2020-12-14 16:34

from django.db import migrations, models
import music_library.models


class Migration(migrations.Migration):

    dependencies = [
        ('music_library', '0003_stand'),
    ]

    operations = [
        migrations.AddField(
            model_name='stand',
            name='score',
            field=models.FileField(default=None, upload_to=music_library.models.stand_file_path, verbose_name='Partition'),
            preserve_default=False,
        ),
    ]