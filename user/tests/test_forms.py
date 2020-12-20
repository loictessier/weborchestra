from django.test import TestCase
from django.contrib.auth.models import User
from django.core import mail
from django.http import HttpRequest

from model_bakery import baker
from unittest.mock import patch

from user.forms import (
    SignupForm, SigninForm, PasswordResetForm, SetPasswordForm,
    EMPTY_EMAIL_ERROR, DUPLICATE_USER_ERROR
)
from user.models import Profile


class SignupFormTest(TestCase):

    def setUp(self):
        self.request = HttpRequest()

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

    def test_form_validation_for_duplicate_active_user(self):
        self.user1 = baker.make(
            User,
            username='test@test.test',
            email='test@test.test',
            is_active=True,
        )
        form = SignupForm(data={
            'email': self.user1.email,
            'password1': 'GoodPassword1234',
            'password2': 'GoodPassword1234'
        })
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['email'], [DUPLICATE_USER_ERROR])

    def test_form_validation_for_duplicate_inactive_user(self):
        self.user1 = baker.make(
            User,
            username='test@test.test',
            email='test@test.test',
            is_active=False,
        )
        form = SignupForm(data={
            'email': self.user1.email,
            'password1': 'GoodPassword1234',
            'password2': 'GoodPassword1234'
        })
        self.assertTrue(form.is_valid())
        self.assertEqual(len(form.errors), 0)

    @patch('user.forms.get_current_site')
    def test_valid_form_create_user(self, mock_get_current_site):
        form = SignupForm(data={
            'email': 'example@email.test',
            'password1': 'GoodPassword1234',
            'password2': 'GoodPassword1234'
        })
        self.assertTrue(form.is_valid())
        form.save(self.request)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(Profile.objects.count(), 1)
        new_profile = Profile.objects.first()
        self.assertEqual(new_profile.user.email, 'example@email.test')
        self.assertFalse(new_profile.user.is_active)

    @patch('user.forms.get_current_site')
    def test_valid_form_send_mail(self, mock_get_current_site):
        form = SignupForm(data={
            'email': 'example@email.test',
            'password1': 'GoodPassword1234',
            'password2': 'GoodPassword1234'
        })
        self.assertTrue(form.is_valid())
        form.save(self.request)
        self.assertEqual(len(mail.outbox), 1)
        sent_mail = mail.outbox[0]
        self.assertIn('example@email.test', sent_mail.body)


class SigninFormTest(TestCase):

    def test_form_renders_email_input(self):
        form = SigninForm()
        self.assertIn('placeholder="exemple@adresse.com"', form.as_p())
        self.assertIn('class="form-control input-lg"', form.as_p())

    def test_form_renders_password_input(self):
        form = SigninForm()
        self.assertIn('placeholder="********', form.as_p())


class PasswordResetFormTest(TestCase):

    def test_form_renders_email_input(self):
        form = PasswordResetForm()
        self.assertIn('placeholder="exemple@adresse.com"', form.as_p())

    def test_form_validation_for_blank_email(self):
        form = PasswordResetForm(data={'email': ''})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['email'], [EMPTY_EMAIL_ERROR])


class SetPasswordFormTest(TestCase):

    def test_form_renders_password_inputs(self):
        form = SetPasswordForm('test@example.com')
        self.assertIn('placeholder="********"', form.as_p())
        self.assertIn('id="id_new_password1"', form.as_p())
        self.assertIn('id="id_new_password2"', form.as_p())
