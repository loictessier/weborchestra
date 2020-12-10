from unittest.mock import patch

from django.test import TestCase
from django.http import HttpRequest

from music_library.views import new_score
from music_library.models import MusicScore


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


@patch('music_library.views.NewScoreForm')
class NewScoreViewUnitTest(TestCase):

    def setUp(self):
        self.request = HttpRequest()
        self.request.POST['name'] = 'T-Bones In Swing'
        self.request.POST['author'] = 'George Gershwin'
        self.request.POST['editor'] = 'Molenaar Edition'

    def test_passes_POST_data_to_NewScoreForm(self, mockNewScoreForm):
        new_score(self.request)
        mockNewScoreForm.assert_called_once_with(data=self.request.POST)

    def test_saves_form_if_form_valid(self, mockNewScoreForm):
        mock_form = mockNewScoreForm.return_value
        mock_form.is_valid.return_value = True
        new_score(self.request)
        mock_form.save.assert_called_once()

    @patch('music_library.views.redirect')
    def test_redirects_to_form_returned_object_if_form_valid(
        self, mock_redirect, mockNewScoreForm
    ):
        mock_form = mockNewScoreForm.return_value
        mock_form.is_valid.return_value = True

        response = new_score(self.request)

        self.assertEqual(response, mock_redirect.return_value)
        mock_redirect.assert_called_once_with(str(mock_form.save.return_value.get_absolute_url()))

    @patch('music_library.views.render')
    def test_renders_new_score_template_with_form_if_form_invalid(
        self, mock_render, mockNewScoreForm
    ):
        mock_form = mockNewScoreForm.return_value
        mock_form.is_valid.return_value = False

        response = new_score(self.request)

        self.assertEqual(response, mock_render.return_value)
        mock_render.assert_called_once_with(
            self.request, 'music_library/new_score.html', {'form': mock_form}
        )

    def test_does_not_save_if_form_invalid(self, mockNewScoreForm):
        mock_form = mockNewScoreForm.return_value
        mock_form.is_valid.return_value = False
        new_score(self.request)
        mock_form.save.assert_not_called()


class ScoreViewIntegratedTest(TestCase):

    def test_uses_score_template(self):
        score = MusicScore.objects.create()
        response = self.client.get(f'/music-library/{score.id}/')
        self.assertTemplateUsed(response, 'music_library/score.html')

    def test_passes_correct_list_to_template(self):
        correct_score = MusicScore.objects.create(
            name='T-Bones In Swing',
            author='George Gershwin',
            editor='Molenaar Edition'
        )
        response = self.client.get(f'/music-library/{correct_score.id}/')
        self.assertEqual(response.context['score'], correct_score)
