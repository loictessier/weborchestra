from django.urls import resolve
from django.test import TestCase
from django.http import HttpRequest
from model_bakery import baker

from user.views import signup

from django.contrib.auth.models import User
from user.models import Profile

from user.forms import EMPTY_EMAIL_ERROR, SignupForm

# Test Views/Templates
class SignupTest(TestCase):

    def test_uses_signup_template(self):
        response = self.client.get('/auth/signup')
        self.assertTemplateUsed(response, 'user/signup.html')

    def test_can_save_a_POST_request(self):
        response = self.client.post('/auth/signup', data={'email': 'example@email.test'})
        self.assertIn('example@email.test', response.content.decode())
        self.assertTemplateUsed(response, 'user/signup.html')

    def test_signup_page_uses_item_form(self):
        response = self.client.get('/auth/signup')
        self.assertIsInstance(response.context['form'], SignupForm)

# Test Models
class ProfileTest(TestCase):
    
    def test_profile_creation(self):
        new_user = baker.make(User)
        new_profile = baker.make(Profile, user=new_user)
        self.assertTrue(isinstance(new_profile, Profile))
        self.assertEqual(new_user.username, new_profile.__str__())

# Test Forms
class SignupFormTest(TestCase):

    def test_form_renders_signup_email_input(self):
        form = SignupForm()
        self.assertIn('placeholder="exemple@adresse.com"', form.as_p())
        self.assertIn('class="form-control input-lg"', form.as_p())

    def test_form_validation_for_blank_items(self):
        form = SignupForm(data={'email': ''})
        self.assertFalse(form.is_valid())
        self.assertEqual(
            form.errors['email'],
            [EMPTY_EMAIL_ERROR]
        )