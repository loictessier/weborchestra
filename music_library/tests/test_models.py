from django.test import TestCase
from django.core.exceptions import ValidationError

from music_library.models import MusicScore, Instrument, Stand, stand_file_path


class StandFilePathUnitTest(TestCase):

    def test_returns_correct_path(self):
        score = MusicScore.objects.create(
            name='T-Bones In Swing',
            author='George Gershwin',
            editor='Molenaar Edition'
        )
        instrument = Instrument.objects.create(
            name='Hautbois',
            music_score=score
        )
        stand = Stand.objects.create(
            name='Hautbois 1',
            instrument=instrument
        )
        response = stand_file_path(stand, 'score_name.pdf')
        self.assertEqual(
            response,
            'partitions/T-Bones In Swing/'
            'Hautbois/T-Bones In Swing-Hautbois 1.pdf'
        )


class MusicScoreModelTest(TestCase):

    def test_get_absolute_url(self):
        music_score = MusicScore.objects.create()
        self.assertEqual(
            music_score.get_absolute_url(),
            f'/music-library/{music_score.id}/'
        )

    def test_string_representation(self):
        MusicScore.objects.create(
            name='T-Bones In Swing',
            author='George Gershwin',
            editor='Molenaar Edition'
        )
        new_score = MusicScore.objects.first()
        self.assertEqual(str(new_score), 'T-Bones In Swing - George Gershwin')


class InstrumentModelTest(TestCase):

    def setUp(self):
        self.score1 = MusicScore.objects.create(
            name='T-Bones In Swing',
            author='George Gershwin',
            editor='Molenaar Edition'
        )
        self.score2 = MusicScore.objects.create(
            name='Adrenalina',
            author='Renato Soglia',
            editor='Scomegna Edizioni Musicali'
        )

    def test_get_absolute_url(self):
        instrument = Instrument.objects.create(music_score=self.score1)
        self.assertEqual(
            instrument.get_absolute_url(),
            f'/music-library/{instrument.music_score.id}/{instrument.id}/'
        )

    def test_string_representation(self):
        Instrument.objects.create(
            name='Hautbois',
            music_score=self.score1
        )
        new_instrument = Instrument.objects.first()
        self.assertEqual(str(new_instrument), 'Hautbois')

    def test_unique_constraint_instrument_score(self):
        Instrument.objects.create(
            name='Hautbois',
            music_score=self.score1
        )
        Instrument.objects.create(
            name='Hautbois',
            music_score=self.score2
        )
        with self.assertRaises(ValidationError):
            instrument = Instrument(
                name='Hautbois',
                music_score=self.score1
            )
            instrument.full_clean()
        self.assertEqual(len(Instrument.objects.all()), 2)


class StandModelTest(TestCase):

    def setUp(self):
        self.score1 = MusicScore.objects.create(
            name='T-Bones In Swing',
            author='George Gershwin',
            editor='Molenaar Edition'
        )
        self.score2 = MusicScore.objects.create(
            name='Adrenalina',
            author='Renato Soglia',
            editor='Scomegna Edizioni Musicali'
        )
        self.instrument1 = Instrument.objects.create(
            name='Hautbois',
            music_score=self.score1
        )
        self.instrument2 = Instrument.objects.create(
            name='Hautbois',
            music_score=self.score2
        )

    def test_get_absolute_url(self):
        music_score = MusicScore.objects.create()
        instrument = Instrument.objects.create(music_score=music_score)
        stand = Stand.objects.create(instrument=instrument)
        self.assertEqual(
            stand.get_absolute_url(),
            f'/music-library/{music_score.id}/{instrument.id}/{stand.id}/'
        )

    def test_string_representation(self):

        Stand.objects.create(
            name='Hautbois 1',
            instrument=self.instrument1
        )
        new_stand = Stand.objects.first()
        self.assertEqual(str(new_stand), 'Hautbois 1')

    def test_unique_constraint_instrument_score(self):
        Stand.objects.create(
            name='Hautbois 1',
            instrument=self.instrument1
        )
        Stand.objects.create(
            name='Hautbois 1',
            instrument=self.instrument2
        )
        with self.assertRaises(ValidationError):
            stand = Stand(
                name='Hautbois 1',
                score='hautbois_1.pdf',
                instrument=self.instrument1
            )
            stand.full_clean()
        self.assertEqual(len(Stand.objects.all()), 2)
