from django.urls import resolve
from django.test import TestCase
from django.http import HttpRequest

from core.views import index

# Create your tests here.
class IndexTest(TestCase):

    def test_root_url_resolves_to_index_view(self):
        found = resolve('/')
        self.assertEqual(found.func, index)

    def test_index_returns_correct_html(self):
        request = HttpRequest()
        response = index(request)
        html = response.content.decode('utf8')
        self.assertIn("<title> Int'Aire'Mezzo | Accueil </title>", html)
