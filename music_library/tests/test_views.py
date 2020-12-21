from unittest.mock import patch

from django.test import TestCase
from django.http import HttpRequest

from music_library.views import new_score, new_instrument, new_stand
from music_library.models import MusicScore, Instrument, Stand


class MusicLibraryViewIntegratedTest(TestCase):

    def test_uses_music_library_template(self):
        response = self.client.get('/music-library/')
        self.assertTemplateUsed(response, 'music_library/music_library.html')

    def test_passes_music_scores_to_template(self):
        new_score = MusicScore.objects.create(
            name='T-Bones In Swing',
            author='George Gershwin',
            editor='Molenaar Edition'
        )
        response = self.client.get('/music-library/')
        music_scores = response.context['music_scores']
        self.assertEqual(music_scores.first(), new_score)
        self.assertEqual(len(music_scores), 1)


@patch('music_library.views.ScoreForm')
class NewScoreViewUnitTest(TestCase):

    def setUp(self):
        self.request = HttpRequest()
        self.request.POST['name'] = 'T-Bones In Swing'
        self.request.POST['author'] = 'George Gershwin'
        self.request.POST['editor'] = 'Molenaar Edition'

    def test_passes_POST_data_to_ScoreForm(self, mock_ScoreForm):
        new_score(self.request)
        mock_ScoreForm.assert_called_once_with(data=self.request.POST)

    def test_saves_form_if_form_valid(self, mock_ScoreForm):
        mock_form = mock_ScoreForm.return_value
        mock_form.is_valid.return_value = True
        new_score(self.request)
        mock_form.save.assert_called_once()

    @patch('music_library.views.redirect')
    def test_redirects_to_form_returned_object_if_form_valid(
        self, mock_redirect, mock_ScoreForm
    ):
        mock_form = mock_ScoreForm.return_value
        mock_form.is_valid.return_value = True

        response = new_score(self.request)

        self.assertEqual(response, mock_redirect.return_value)
        mock_redirect.assert_called_once_with(
            str(mock_form.save.return_value.get_absolute_url())
        )

    @patch('music_library.views.render')
    def test_renders_new_score_template_with_form_if_form_invalid(
        self, mock_render, mock_ScoreForm
    ):
        mock_form = mock_ScoreForm.return_value
        mock_form.is_valid.return_value = False

        response = new_score(self.request)

        self.assertEqual(response, mock_render.return_value)
        mock_render.assert_called_once_with(
            self.request, 'music_library/new_score.html', {'form': mock_form}
        )

    def test_does_not_save_if_form_invalid(self, mock_ScoreForm):
        mock_form = mock_ScoreForm.return_value
        mock_form.is_valid.return_value = False
        new_score(self.request)
        mock_form.save.assert_not_called()


class ScoreViewIntegratedTest(TestCase):

    def test_uses_score_template(self):
        score = MusicScore.objects.create()
        response = self.client.get(f'/music-library/{score.id}/')
        self.assertTemplateUsed(response, 'music_library/score.html')

    def test_passes_correct_score_and_instruments_to_template(self):
        correct_score = MusicScore.objects.create(
            name='T-Bones In Swing',
            author='George Gershwin',
            editor='Molenaar Edition'
        )
        Instrument.objects.create(
            name='Hautbois',
            music_score=correct_score
        )
        Instrument.objects.create(
            name='Trompette',
            music_score=MusicScore.objects.create()
        )
        response = self.client.get(f'/music-library/{correct_score.id}/')
        self.assertEqual(response.context['score'], correct_score)
        self.assertEqual(len(response.context['instruments']), 1)


@patch('music_library.views.InstrumentForm')
class NewInstrumentViewUnitTest(TestCase):

    def setUp(self):
        self.request = HttpRequest()
        self.request.POST['name'] = 'Hautbois'
        self.music_score = MusicScore.objects.create(
            name='T-Bones In Swing',
            author='George Gershwin',
            editor='Molenaar Edition'
        )

    def test_passes_POST_data_to_InstrumentForm(
        self, mock_InstrumentForm
    ):
        new_instrument(self.request, self.music_score.id)
        mock_InstrumentForm.assert_called_once_with(
            music_score=self.music_score,
            data=self.request.POST
        )

    def test_saves_form_if_form_valid(self, mock_InstrumentForm):
        mock_form = mock_InstrumentForm.return_value
        mock_form.is_valid.return_value = True
        new_instrument(self.request, self.music_score.id)
        mock_form.save.assert_called_once()

    @patch('music_library.views.redirect')
    def test_redirects_to_form_returned_object_if_form_valid(
        self, mock_redirect, mock_InstrumentForm
    ):
        mock_form = mock_InstrumentForm.return_value
        mock_form.is_valid.return_value = True
        response = new_instrument(self.request, self.music_score.id)
        self.assertEqual(response, mock_redirect.return_value)
        mock_redirect.assert_called_once_with(
            str(mock_form.save.return_value.get_absolute_url())
        )

    @patch('music_library.views.render')
    def test_renders_new_instrument_template_if_form_invalid(
        self, mock_render, mock_InstrumentForm
    ):
        mock_form = mock_InstrumentForm.return_value
        mock_form.is_valid.return_value = False
        response = new_instrument(self.request, self.music_score.id)
        self.assertEqual(response, mock_render.return_value)
        mock_render.assert_called_once_with(
            self.request,
            'music_library/new_instrument.html',
            {'form': mock_form}
        )

    def test_does_not_save_if_form_invalid(self, mock_InstrumentForm):
        mock_form = mock_InstrumentForm.return_value
        mock_form.is_valid.return_value = False
        new_instrument(self.request, self.music_score.id)
        mock_form.save.assert_not_called()


class InstrumentViewIntegratedTest(TestCase):

    def test_uses_instrument_template(self):
        score = MusicScore.objects.create()
        instrument = Instrument.objects.create(music_score=score)
        response = self.client.get(
            f'/music-library/{score.id}/{instrument.id}/'
        )
        self.assertTemplateUsed(response, 'music_library/instrument.html')

    def test_passes_correct_arguments_to_template(self):
        correct_score = MusicScore.objects.create(
            name='T-Bones In Swing',
            author='George Gershwin',
            editor='Molenaar Edition'
        )
        correct_instrument = Instrument.objects.create(
            name='Hautbois',
            music_score=correct_score
        )
        Stand.objects.create(
            name='Hautbois 1',
            instrument=correct_instrument
        )
        Stand.objects.create(
            name='Trompette 1',
            instrument=Instrument.objects.create(
                name='Trompette',
                music_score=correct_score
            )
        )
        response = self.client.get(
            f'/music-library/{correct_score.id}/{correct_instrument.id}/'
        )
        self.assertEqual(response.context['score'], correct_score)
        self.assertEqual(response.context['instrument'], correct_instrument)
        self.assertEqual(len(response.context['stands']), 1)


@patch('music_library.views.StandForm')
class NewStandViewUnitTest(TestCase):

    def setUp(self):
        self.request = HttpRequest()
        self.music_score = MusicScore.objects.create(
            name='T-Bones In Swing',
            author='George Gershwin',
            editor='Molenaar Edition'
        )
        self.instrument = Instrument.objects.create(
            name='Hautbois',
            music_score=self.music_score
        )
        self.request.POST['name'] = f'{self.instrument.name} 1'

    def test_passes_POST_data_to_StandForm(
        self, mock_StandForm
    ):
        new_stand(self.request, self.music_score.id, self.instrument.id)
        mock_StandForm.assert_called_once_with(
            instrument=self.instrument,
            data=self.request.POST,
            files=self.request.FILES
        )

    def test_saves_form_if_form_valid(self, mock_StandForm):
        mock_form = mock_StandForm.return_value
        mock_form.is_valid.return_value = True
        new_stand(self.request, self.music_score.id, self.instrument.id)
        mock_form.save.assert_called_once()

    @patch('music_library.views.redirect')
    def test_redirects_to_form_returned_object_if_form_valid(
        self, mock_redirect, mock_StandForm
    ):
        mock_form = mock_StandForm.return_value
        mock_form.is_valid.return_value = True
        response = new_stand(
            self.request,
            self.music_score.id,
            self.instrument.id
        )
        self.assertEqual(response, mock_redirect.return_value)
        mock_redirect.assert_called_once_with(
            str(mock_form.save.return_value.get_absolute_url())
        )

    @patch('music_library.views.render')
    def test_renders_new_stand_template_if_form_invalid(
        self, mock_render, mock_StandForm
    ):
        mock_form = mock_StandForm.return_value
        mock_form.is_valid.return_value = False
        response = new_stand(
            self.request,
            self.music_score.id,
            self.instrument.id
        )
        self.assertEqual(response, mock_render.return_value)
        mock_render.assert_called_once_with(
            self.request,
            'music_library/new_stand.html',
            {'form': mock_form}
        )

    def test_does_not_save_if_form_invalid(self, mock_StandForm):
        mock_form = mock_StandForm.return_value
        mock_form.is_valid.return_value = False
        new_stand(self.request, self.music_score.id, self.instrument.id)
        mock_form.save.assert_not_called()


@patch('music_library.views.Stand.score')
class StandViewIntegratedTest(TestCase):

    def test_uses_stand_template(self, mock_stand_score):
        score = MusicScore.objects.create()
        instrument = Instrument.objects.create(music_score=score)
        stand = Stand.objects.create(instrument=instrument)
        response = self.client.get(
            f'/music-library/{score.id}/{instrument.id}/{stand.id}/'
        )
        self.assertTemplateUsed(response, 'music_library/stand.html')

    def test_passes_correct_instrument_and_score_to_template(
        self, mock_stand_score
    ):
        correct_score = MusicScore.objects.create(
            name='T-Bones In Swing',
            author='George Gershwin',
            editor='Molenaar Edition'
        )
        correct_instrument = Instrument.objects.create(
            name='Hautbois',
            music_score=correct_score
        )
        correct_stand = Stand.objects.create(
            name='Hautbois1',
            instrument=correct_instrument
        )
        response = self.client.get(
            f'/music-library/{correct_score.id}/'
            f'{correct_instrument.id}/{correct_stand.id}/'
        )
        self.assertEqual(response.context['score'], correct_score)
        self.assertEqual(response.context['instrument'], correct_instrument)
        self.assertEqual(response.context['stand'], correct_stand)
