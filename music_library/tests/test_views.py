from django.test import TestCase


class MusicLibraryViewIntegratedTest(TestCase):

    def test_uses_music_library_template(self):
        response = self.client.get('/music-library/')
        self.assertTemplateUsed(response, 'music_library/music_library.html')
