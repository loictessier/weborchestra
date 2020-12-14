from pathlib import Path

from django.db import models
from django.urls import reverse


def stand_file_path(instance, filename):
    extension = ''.join(Path(filename).suffixes)
    return (f'partitions/{instance.instrument.music_score.name}/'
            f'{instance.instrument.name}/'
            f'{instance.instrument.music_score.name}-{instance.name}{extension}')


# Create your models here.
class MusicScore(models.Model):
    name = models.TextField('Nom', max_length=50, unique=True)
    author = models.TextField('Auteur', max_length=50, unique=False)
    editor = models.TextField('Editeur', max_length=50, unique=False)

    def get_absolute_url(self):
        return reverse('music_library:view_score', args=[self.id])

    def __str__(self):
        return f'{self.name} - {self.author}'


class Instrument(models.Model):
    name = models.TextField('Nom', max_length=50, unique=True)
    music_score = models.ForeignKey('MusicScore', on_delete=models.CASCADE)

    def get_absolute_url(self):
        return reverse('music_library:view_instrument', args=[self.music_score.id, self.id])

    def __str__(self):
        return f'{self.name}'


class Stand(models.Model):
    name = models.TextField('Nom', max_length=50, unique=True)
    score = models.FileField(verbose_name='Partition', upload_to=stand_file_path)
    instrument = models.ForeignKey('Instrument', on_delete=models.CASCADE)

    def get_absolute_url(self):
        return reverse('music_library:view_stand', args=[self.instrument.music_score.id, self.instrument.id, self.id])

    def __str__(self):
        return f'{self.name}'
