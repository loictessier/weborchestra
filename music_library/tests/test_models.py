from django.test import TestCase

from music_library.models import MusicScore


class MusicScoreModelTest(TestCase):

    def test_get_absolute_url(self):
        music_score = MusicScore.objects.create()
        self.assertEqual(
            music_score.get_absolute_url(),
            f'/music-library/{music_score.id}/'
        )

    def test_create_new_creates_music_score(self):
        new_score = MusicScore.create_new(
            name='T-Bones In Swing',
            author='George Gershwin',
            editor='Molenaar Edition'
        )
        self.assertEqual(new_score.name, 'T-Bones In Swing')
        self.assertEqual(new_score.author, 'George Gershwin')
        self.assertEqual(new_score.editor, 'Molenaar Edition')

    def test_string_representation(self):
        MusicScore.create_new(
            name='T-Bones In Swing',
            author='George Gershwin',
            editor='Molenaar Edition'
        )
        new_score = MusicScore.objects.first()
        self.assertEqual(str(new_score), 'T-Bones In Swing - George Gershwin')
