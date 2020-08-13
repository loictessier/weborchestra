from django.urls import resolve
from django.test import TestCase
from django.http import HttpRequest

from user.views import signup

# Create your tests here.
class SignupTest(TestCase):

    def test_signup_url_resolves_to_signup(self):
        found = resolve('/auth/signup')
        self.assertEqual(found.func, signup)

    def test_signup_returns_correct_html(self):
        request = HttpRequest()
        response = signup(request)
        html = response.content.decode('utf8')
        self.assertIn("<title> Int'Aire'Mezzo | S'inscrire </title>", html)
