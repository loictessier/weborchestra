from unittest.mock import patch, Mock, MagicMock

from django.utils.html import escape
from django.test import TestCase

from music_library.forms import ScoreForm, InstrumentForm, StandForm


class ScoreFormTest(TestCase):

    def test_form_render_inputs(self):
        form = ScoreForm(data={})
        self.assertIn('id="id_name"', form.as_p())
        self.assertIn('placeholder="Nom de la partition"', form.as_p())
        self.assertIn('id="id_author"', form.as_p())
        author_placeholder = escape("Nom de l'auteur")
        self.assertIn(f'placeholder="{author_placeholder}"', form.as_p())
        self.assertIn('id="id_editor"', form.as_p())
        editor_placeholder = escape("Nom de l'éditeur")
        self.assertIn(f'placeholder="{editor_placeholder}"', form.as_p())

    @patch('music_library.forms.MusicScore')
    def test_save_returns_new_score_from_post_data(
        self, mock_MusicScore
    ):
        form = ScoreForm(data={
            'name': 'T-Bones In Swing',
            'author': 'George Gershwin',
            'editor': 'Molenaar Edition'
        })
        form.is_valid()
        response = form.save()
        self.assertEqual(
            response,
            mock_MusicScore.objects.create.return_value
        )
        mock_MusicScore.objects.create.assert_called_once_with(
            name='T-Bones In Swing',
            author='George Gershwin',
            editor='Molenaar Edition'
        )


class InstrumentFormtest(TestCase):

    def setUp(self):
        self.music_score = Mock()

    def test_form_render_inputs(self):
        form = InstrumentForm(data={})
        self.assertIn('id="id_name"', form.as_p())
        name_placeholder = escape("Nom de l'instrument")
        self.assertIn(f'placeholder="{name_placeholder}"', form.as_p())

    @patch('music_library.forms.Instrument')
    def test_save_returns_new_instrument_from_post_data(
        self, mock_Instrument
    ):
        form = InstrumentForm(data={
            'name': 'Hautbois'
        })
        form.is_valid()
        form.save(self.music_score)
        mock_Instrument.objects.create.assert_called_once_with(
            name='Hautbois',
            music_score=self.music_score
        )


class StandFormtest(TestCase):

    def setUp(self):
        self.music_score = Mock()
        self.instrument = Mock(music_score=self.music_score)

    def test_form_render_inputs(self):
        form = StandForm(data={})
        self.assertIn('id="id_name"', form.as_p())
        self.assertIn('placeholder="Nom du pupitre"', form.as_p())

    @patch('music_library.forms.Stand')
    def test_save_returns_new_stand_from_post_data(
        self, mock_Stand
    ):
        mock_file = MagicMock(name='hautbois1.pdf')
        form = StandForm(
            data={
                'name': 'Hautbois 1'
            },
            files={
                'score': mock_file
            }
        )
        form.is_valid()
        form.save(self.instrument)
        mock_Stand.objects.create.assert_called_once_with(
            name='Hautbois 1',
            score=mock_file,
            instrument=self.instrument
        )
