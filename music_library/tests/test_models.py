from django.test import TestCase

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
        self.assertEqual(response, 'partitions/T-Bones In Swing/Hautbois/T-Bones In Swing-Hautbois 1.pdf')


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

    def test_get_absolute_url(self):
        music_score = MusicScore.objects.create()
        instrument = Instrument.objects.create(music_score=music_score)
        self.assertEqual(
            instrument.get_absolute_url(),
            f'/music-library/{instrument.music_score.id}/{instrument.id}/'
        )

    def test_string_representation(self):
        score = MusicScore.objects.create(
            name='T-Bones In Swing',
            author='George Gershwin',
            editor='Molenaar Edition'
        )
        Instrument.objects.create(
            name='Hautbois',
            music_score=score
        )
        new_instrument = Instrument.objects.first()
        self.assertEqual(str(new_instrument), 'Hautbois')


class StandModelTest(TestCase):

    def test_get_absolute_url(self):
        music_score = MusicScore.objects.create()
        instrument = Instrument.objects.create(music_score=music_score)
        stand = Stand.objects.create(instrument=instrument)
        self.assertEqual(
            stand.get_absolute_url(),
            f'/music-library/{music_score.id}/{instrument.id}/{stand.id}/'
        )

    def test_string_representation(self):
        score = MusicScore.objects.create(
            name='T-Bones In Swing',
            author='George Gershwin',
            editor='Molenaar Edition'
        )
        instrument = Instrument.objects.create(
            name='Hautbois',
            music_score=score
        )
        Stand.objects.create(
            name='Hautbois 1',
            instrument=instrument
        )
        new_stand = Stand.objects.first()
        self.assertEqual(str(new_stand), 'Hautbois 1')
