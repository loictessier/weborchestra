from django.test import TestCase


class IndexTest(TestCase):

    def test_index_returns_correct_html(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'core/index.html')
