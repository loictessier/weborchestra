from unittest.mock import patch

from django.utils.html import escape
from django.test import TestCase

from music_library.forms import ScoreForm, NewScoreForm


class ScoreFormTest(TestCase):

    def test_form_render_inputs(self):
        form = ScoreForm(data={})
        self.assertIn('id="id_name"', form.as_p())
        self.assertIn('placeholder="Nom de la partition"', form.as_p())
        self.assertIn('id="id_author"', form.as_p())
        self.assertIn('placeholder="' + escape("Nom de l'auteur"), form.as_p())
        self.assertIn('id="id_editor"', form.as_p())
        self.assertIn('placeholder="' + escape("Nom de l'éditeur"), form.as_p())


@patch('music_library.forms.MusicScore.create_new')
class NewScoreFormTest(TestCase):

    def test_save_returns_new_score(
        self, mock_MusicScore_create_new
    ):
        form = NewScoreForm(data={
            'name': 'T-Bones In Swing',
            'author': 'George Gershwin',
            'editor': 'Molenaar Edition'
        })
        form.is_valid()
        form.save()

    def test_save_creates_new_score_from_post_data(
        self, mock_MusicScore_create_new
    ):
        # mock_music_score = mockMusicScore.return_value
        form = NewScoreForm(data={
            'name': 'T-Bones In Swing',
            'author': 'George Gershwin',
            'editor': 'Molenaar Edition'
        })
        form.is_valid()
        music_score = form.save()
        self.assertEqual(
            music_score,
            mock_MusicScore_create_new.return_value
        )
