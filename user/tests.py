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

    def test_only_saves_profile_when_necessary(self):
        self.client.get('/auth/signup')
        self.assertEqual(Profile.objects.count(), 0)

    def test_can_save_a_POST_request(self):
        self.client.post('/auth/signup', data={'email': 'example@email.test'})

        self.assertEqual(Profile.objects.count(), 1)
        new_profile = Profile.objects.first()
        self.assertEqual(new_profile.user.email, 'example@email.test')

    def test_redirects_after_POST(self):
        response = self.client.post('/auth/signup', data={'email': 'example@email.test'})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['location'], '/')

    def test_signup_page_uses_signup_form(self):
        response = self.client.get('/auth/signup')
        self.assertIsInstance(response.context['form'], SignupForm)

# Test Models
class ProfileTest(TestCase):
    
    def test_saving_and_retrieving_profiles(self):
        first_user = baker.make(User)
        first_profile = baker.make(Profile, user=first_user)
        second_user = baker.make(User)
        second_profile = baker.make(Profile, user= second_user)

        saved_profiles = Profile.objects.all()
        self.assertEqual(saved_profiles.count(), 2)

        first_saved_profile = saved_profiles[0]
        self.assertTrue(isinstance(first_saved_profile, Profile))
        self.assertEqual(first_user.username, first_saved_profile.__str__())

# Test Forms
class SignupFormTest(TestCase):

    def test_form_renders_email_input(self):
        form = SignupForm()
        self.assertIn('placeholder="exemple@adresse.com"', form.as_p())
        self.assertIn('class="form-control input-lg"', form.as_p())

    def test_form_renders_password_and_confirm_inputs(self):
        form = SignupForm()
        self.assertIn('placeholder="********"', form.as_p())
        self.assertIn('id="id_password1', form.as_p())
        self.assertIn('id="id_password2"', form.as_p())

    def test_form_validation_for_blank_items(self):
        form = SignupForm(data={'email': ''})
        self.assertFalse(form.is_valid())
        self.assertEqual(
            form.errors['email'],
            [EMPTY_EMAIL_ERROR]
        )

    def test_form_validation_for_password_mismatch(self):
        form = SignupForm(data={
            'email': 'test@test.test',
            'password1': 'abcdef123',
            'password2': 'badcfe321'
        })
        self.assertFalse(form.is_valid())
        self.assertEqual(
            form.errors['password2'],
            ['Les deux mots de passe ne correspondent pas.']
        )