from django.test import TestCase
from django.contrib.auth.models import User
from model_bakery import baker

from user.forms import (
    SignupForm, SigninForm,
    EMPTY_EMAIL_ERROR, DUPLICATE_USER_ERROR
)


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


class SigninFormTest(TestCase):

    def test_form_renders_email_input(self):
        form = SigninForm()
        self.assertIn('placeholder="exemple@adresse.com"', form.as_p())
        self.assertIn('class="form-control input-lg"', form.as_p())

    def test_form_renders_password_input(self):
        form = SigninForm()
        self.assertIn('placeholder="********', form.as_p())
