from django.urls import resolve
from django.test import TestCase
from django.http import HttpRequest
from django.utils.html import escape
from model_bakery import baker

from user.views import signup

from django.contrib.auth.models import User
from user.models import Profile

from user.forms import EMPTY_EMAIL_ERROR, DUPLICATE_USER_ERROR, SignupForm

# Test Views/Templates
class SignupTest(TestCase):

    def test_uses_signup_template(self):
        response = self.client.get('/auth/signup')
        self.assertTemplateUsed(response, 'user/signup.html')

    def test_only_saves_profile_when_necessary(self):
        self.client.get('/auth/signup')
        self.assertEqual(Profile.objects.count(), 0)

    def test_signup_page_uses_signup_form(self):
        response = self.client.get('/auth/signup')
        self.assertIsInstance(response.context['form'], SignupForm)

    def test_for_invalid_input_renders_signup_templates(self):
        response = self.client.post('/auth/signup', data={'email': ''})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'user/signup.html')

    def test_validation_errors_are_shown_on_signup_page(self):
        response = self.client.post('/auth/signup', data={'email': ''})
        self.assertContains(response, escape(EMPTY_EMAIL_ERROR))

    def test_for_invalid_input_passes_form_to_template(self):
        response = self.client.post('/auth/signup', data={'email': ''})
        self.assertIsInstance(response.context['form'], SignupForm)

    def test_can_save_a_POST_request(self):
        self.client.post('/auth/signup', data={
            'email': 'example@email.test',
            'password1': 'Django4521',
            'password2': 'Django4521'
        })
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(Profile.objects.count(), 1)
        new_profile = Profile.objects.first()
        self.assertEqual(new_profile.user.email, 'example@email.test')

    def test_redirects_after_POST(self):
        response = self.client.post('/auth/signup', data={
            'email': 'example@email.test',
            'password1': 'Django4521',
            'password2': 'Django4521'
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['location'], '/')


# Test Models
class ProfileTest(TestCase):
    
    def test_saving_and_retrieving_profiles(self):
        first_user = baker.make(User)
        second_user = baker.make(User)

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

    def test_form_renders_password1_and_password2_inputs(self):
        form = SignupForm()
        self.assertIn('placeholder="********"', form.as_p())
        self.assertIn('id="id_password1', form.as_p())
        self.assertIn('id="id_password2"', form.as_p())

    def test_form_validation_for_blank_email(self):
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

    def test_form_validation_for_duplicate_user(self):
        self.user1 = baker.make(User, username='test@test.test', email='test@test.test')
        form = SignupForm(data={
            'email': self.user1.email,
            'password1': 'abcdef123',
            'password2': 'abcdef123'
        })
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['email'], [DUPLICATE_USER_ERROR])