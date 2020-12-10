from django.db import models
from django.urls import reverse


# Create your models here.
class MusicScore(models.Model):
    name = models.TextField('Nom', max_length=50, unique=True)
    author = models.TextField('Auteur', max_length=50, unique=False)
    editor = models.TextField('Editeur', max_length=50, unique=False)

    def get_absolute_url(self):
        return reverse('music_library:view_score', args=[self.id])

    @staticmethod
    def create_new(name, author, editor):
        return MusicScore.objects.create(
            name=name,
            author=author,
            editor=editor
        )

    def __str__(self):
        return f'{self.name} - {self.author}'
