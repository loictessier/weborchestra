import os
from pathlib import Path

from django.db import models
from django.urls import reverse
from django.dispatch import receiver


def stand_file_path(instance, filename):
    extension = ''.join(Path(filename).suffixes)
    return (f'partitions/{instance.instrument.music_score.name}/'
            f'{instance.instrument.name}/'
            f'{instance.instrument.music_score.name}-'
            f'{instance.name}{extension}')


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
    name = models.TextField('Nom', max_length=50)
    music_score = models.ForeignKey('MusicScore', on_delete=models.CASCADE)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['name', 'music_score'],
                name='unique_score_instrument_name'
            )
        ]

    def get_absolute_url(self):
        return reverse(
            'music_library:view_instrument',
            args=[self.music_score.id, self.id]
        )

    def __str__(self):
        return f'{self.name}'


class Stand(models.Model):
    name = models.TextField('Nom', max_length=50)
    score = models.FileField(
        verbose_name='Partition',
        upload_to=stand_file_path
    )
    instrument = models.ForeignKey('Instrument', on_delete=models.CASCADE)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['name', 'instrument'],
                name='unique_instrument_stand_name'
            )
        ]

    def get_absolute_url(self):
        return reverse(
            'music_library:view_stand',
            args=[self.instrument.music_score.id, self.instrument.id, self.id]
        )

    def __str__(self):
        return f'{self.name}'


@receiver(models.signals.post_delete, sender=Stand)
def auto_delete_file_on_Stand_delete(sender, instance, **kwargs):
    """
    Deletes file from filesystem
    when corresponding `MediaFile` object is deleted.
    """
    if instance.score:
        if os.path.isfile(instance.score.name):
            os.remove(instance.score.name)


@receiver(models.signals.pre_save, sender=Stand)
def auto_delete_file_on_Stand_change(sender, instance, **kwargs):
    """
    Deletes old file from filesystem
    when corresponding `MediaFile` object is updated
    with new file.
    """
    if not instance.pk:
        return False

    try:
        old_file = Stand.objects.get(pk=instance.pk).score
    except Stand.DoesNotExist:
        return False

    new_file = instance.score
    if not old_file == new_file:
        if os.path.isfile(old_file.name):
            os.remove(old_file.name)
