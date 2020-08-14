from django.urls import resolve
from django.test import TestCase
from django.http import HttpRequest

from user.views import signup

# Create your tests here.
class SignupTest(TestCase):

    def test_signup_returns_correct_html(self):
        response = self.client.get('/auth/signup')
        self.assertTemplateUsed(response, 'user/signup.html')
