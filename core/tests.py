from django.urls import resolve
from django.test import TestCase
from django.http import HttpRequest

from core.views import index

# Create your tests here.
class IndexTest(TestCase):

    def test_index_returns_correct_html(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'core/index.html')
