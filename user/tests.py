from django.urls import resolve, reverse
from django.test import TestCase
from django.http import HttpRequest
from django.utils.html import escape
from model_bakery import baker
from django.core import mail
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from unittest.mock import patch

from user.tokens import account_activation_token

from user.views import ACCOUNT_ACTIVATION_EMAIL_SUBJECT, signup

from django.contrib.auth.models import User
from user.models import Profile

from user.forms import EMPTY_EMAIL_ERROR, DUPLICATE_USER_ERROR, SignupForm, SigninForm

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
        self.assertFalse(new_profile.user.is_active)

    def test_send_mail_after_POST(self):
        response = self.client.post('/auth/signup', data={
            'email': 'example@email.test',
            'password1': 'Django4521',
            'password2': 'Django4521'
        })
        self.assertEqual(len(mail.outbox), 1)
        sent_mail = mail.outbox[0]
        self.assertEqual(sent_mail.subject, ACCOUNT_ACTIVATION_EMAIL_SUBJECT)
        self.assertIn('example@email.test', sent_mail.body)

    def test_redirects_after_POST(self):
        response = self.client.post('/auth/signup', data={
            'email': 'example@email.test',
            'password1': 'Django4521',
            'password2': 'Django4521'
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['location'], '/auth/sent')


class ActivationSentTest(TestCase):

    def test_uses_activation_sent_template(self):
        response = self.client.get('/auth/sent')
        self.assertTemplateUsed(response, 'user/activation_sent.html')


class ActivateTest(TestCase):
    
    def setUp(self):
        self.new_user_data = {
            'email': 'example@email.test',
            'password': 'Django4521'
        }
        self.new_user = User.objects.create_user(
            self.new_user_data['email'],
            self.new_user_data['email'],
            self.new_user_data['password']
        )
        self.new_user.is_active = False
        self.new_user.save()
        self.new_user_data['uid'] = urlsafe_base64_encode(force_bytes(self.new_user.pk))
        self.new_user_data['token'] = account_activation_token.make_token(self.new_user)

    def test_uses_activation_invalid_template_fake_data(self):
        response = self.client.get(reverse('user:activate', kwargs={
            'uidb64': 'FAke-uid_48F23E24022E',
            'token': 'TEST_1337_Fake'
        }))
        self.assertTemplateUsed(response, 'user/activation_invalid.html')

    def test_redirect_index_and_user_active_valid_data(self):
        response = self.client.get(reverse('user:activate', kwargs={
            'uidb64': self.new_user_data['uid'],
            'token': self.new_user_data['token']
        }))
        my_user = User.objects.get(pk=self.new_user.pk)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['location'], '/')
        self.assertTrue(my_user.is_active)
        self.assertTrue(my_user.profile.signup_confirmation)


class SigninTest(TestCase):

    def setUp(self):
        self.new_user = User.objects.create_user('django@test.test', 'django@test.test', 'Django4321')
        self.new_user.is_active = True
        self.new_user.profile.signup_confirmation = True
        self.new_user.save()

    def test_uses_signin_template(self):
        response = self.client.get('/auth/signin')
        self.assertTemplateUsed(response, 'user/signin.html')

    def test_uses_signin_form(self):
        response = self.client.get('/auth/signin')
        self.assertIsInstance(response.context['form'], SigninForm)

    def test_POST_invalid_credentials(self):
        response = self.client.post('/auth/signin', data={
            'email': 'inexistant@email.com',
            'password': 'P4ssw0rd1234'
        })
        self.assertTrue(response.context['authentication_error'])

    def test_POST_valid_credentials_redirect_index(self):
        response = self.client.post('/auth/signin', data={
            'email': 'django@test.test',
            'password': 'Django4321'
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['location'], '/')


class SignoutTest(TestCase):

    def test_redirect_to_index(self):
        response = self.client.get('/auth/signout')
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['location'], '/')

    @patch('user.views.logout')
    def test_user_logged_out(self, mock_logout):
        mock_logout.return_value = None
        response = self.client.get('/auth/signout')
        mock_logout.assert_called_once()


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

    def test_new_profile_set_signup_confirmation_to_false(self):
        new_user = baker.make(User)
        new_profile = new_user.profile

        self.assertFalse(new_profile.signup_confirmation, False)


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


class SigninFormTest(TestCase):

    def test_form_renders_email_input(self):
        form = SigninForm()
        self.assertIn('placeholder="exemple@adresse.com"', form.as_p())
        self.assertIn('class="form-control input-lg"', form.as_p())

    def test_form_renders_password_input(self):
        form = SigninForm()
        self.assertIn('placeholder="********', form.as_p())
