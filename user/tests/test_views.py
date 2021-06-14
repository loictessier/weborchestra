from django.test import TestCase
from django.utils.html import escape
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.core import mail
from django.urls import reverse
from django.http import HttpRequest

from unittest.mock import patch

from user.models import Profile, Role
from user.views import (
    password_reset, signup, informations,
    admin, edit_user
)
from user.forms import (
    SignupForm, SigninForm, PasswordResetForm,
    EMPTY_EMAIL_ERROR
)
from user.tokens import account_activation_token


def _create_user_with_roles(roles):
    new_user = Profile.objects.create_user(
        'edith@example.com',
        'edith@example.com',
        'Django4321'
    )
    new_user.is_active = True
    new_user.signup_confirmation = True
    new_user.save()
    new_user.roles.add(roles)
    return new_user


class SignupViewIntegratedTest(TestCase):

    def test_uses_signup_template(self):
        response = self.client.get('/auth/signup')
        self.assertTemplateUsed(response, 'user/signup.html')

    def test_only_saves_profile_when_necessary(self):
        self.client.get('/auth/signup')
        self.assertEqual(Profile.objects.count(), 0)

    def test_signup_page_uses_signup_form(self):
        response = self.client.get('/auth/signup')
        self.assertIsInstance(response.context['form'], SignupForm)

    def test_validation_errors_are_shown_on_signup_page(self):
        response = self.client.post('/auth/signup', data={'email': ''})
        self.assertContains(response, escape(EMPTY_EMAIL_ERROR))

    def test_for_invalid_input_passes_form_to_template(self):
        response = self.client.post('/auth/signup', data={'email': ''})
        self.assertIsInstance(response.context['form'], SignupForm)
        self.assertTemplateUsed(response, 'user/signup.html')

    def test_redirects_after_POST(self):
        response = self.client.post('/auth/signup', data={
            'email': 'example@email.test',
            'password1': 'Django4521',
            'password2': 'Django4521'
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['location'], '/auth/sent')


@patch('user.views.SignupForm')
class SignupViewUnitTest(TestCase):

    def setUp(self):
        self.request = HttpRequest()
        self.request.POST['email'] = 'edith@example.com'

    def test_call_form_save_if_form_valid(self, mockSignupForm):
        mock_form = mockSignupForm.return_value
        mock_form.is_valid.return_value = True
        signup(self.request)
        mock_form.save.assert_called_once()

    @patch('user.views.redirect')
    def test_render_password_reset_sent_if_form_valid(
        self, mock_redirect, mockSignupForm
    ):
        mock_form = mockSignupForm.return_value
        mock_form.is_valid.return_value = True

        response = signup(self.request)

        self.assertEqual(response, mock_redirect.return_value)
        mock_redirect.assert_called_once_with('/auth/sent')

    @patch('user.views.render')
    def test_renders_password_reset_with_form_if_form_invalid(
        self, mock_render, mockSignupForm
    ):
        mock_form = mockSignupForm.return_value
        mock_form.is_valid.return_value = False

        response = signup(self.request)

        self.assertEqual(response, mock_render.return_value)
        mock_render.assert_called_once_with(
            self.request,
            'user/signup.html',
            {'form': mock_form}
        )


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
        self.new_user = Profile.objects.create_user(
            self.new_user_data['email'],
            self.new_user_data['email'],
            self.new_user_data['password']
        )
        self.new_user.is_active = False
        self.new_user.save()
        self.new_user_data['uid'] = urlsafe_base64_encode(
            force_bytes(self.new_user.pk)
        )
        self.new_user_data['token'] = account_activation_token.make_token(
            self.new_user
        )

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
        my_user = Profile.objects.get(pk=self.new_user.pk)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['location'], '/')
        self.assertTrue(my_user.is_active)
        self.assertTrue(my_user.signup_confirmation)


class SigninTest(TestCase):

    def setUp(self):
        self.new_user = Profile.objects.create_user(
            'django@test.test',
            'django@test.test',
            'Django4321'
        )
        self.new_user.is_active = True
        self.new_user.signup_confirmation = True
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
        self.client.get('/auth/signout')
        mock_logout.assert_called_once()


class PasswordResetViewIntegratedTest(TestCase):

    def setUp(self):
        self.new_user = Profile.objects.create_user(
            'edith@example.com',
            'edith@example.com',
            'Django4321'
        )
        self.new_user.is_active = True
        self.new_user.signup_confirmation = True
        self.new_user.save()

    def test_uses_password_reset_form(self):
        response = self.client.get('/auth/password_reset')
        self.assertIsInstance(response.context['form'], PasswordResetForm)

    def test_can_send_a_mail_if_user_exists(self):
        self.client.post(
            '/auth/password_reset',
            {'email': 'edith@example.com'}
        )
        self.assertEqual(len(mail.outbox), 1)
        sent_mail = mail.outbox[0]
        self.assertIn('edith@example.com', sent_mail.body)

    def test_for_invalid_input_doesnt_send_email_but_shows_errors(self):
        response = self.client.post('/auth/password_reset', data={'email': ''})
        self.assertEqual(len(mail.outbox), 0)
        self.assertContains(response, escape(EMPTY_EMAIL_ERROR))


@patch('user.views.PasswordResetForm')
class PasswordResetViewUnitTest(TestCase):

    def setUp(self):
        self.request = HttpRequest()
        self.request.POST['email'] = 'edith@example.com'

    def test_passes_POST_data_to_PasswordResetForm(
        self, mockPasswordResetForm
    ):
        password_reset(self.request)
        mockPasswordResetForm.assert_called_once_with(data=self.request.POST)

    def test_call_form_save_if_form_valid(self, mockPasswordResetForm):
        mock_form = mockPasswordResetForm.return_value
        mock_form.is_valid.return_value = True
        password_reset(self.request)
        mock_form.save.assert_called_once()

    @patch('user.views.render')
    def test_render_password_reset_sent_if_form_valid(
        self, mock_render, mockPasswordResetForm
    ):
        mock_form = mockPasswordResetForm.return_value
        mock_form.is_valid.return_value = True

        response = password_reset(self.request)

        self.assertEqual(response, mock_render.return_value)
        mock_render.assert_called_once_with(
            self.request,
            'registration/password_reset_done.html',
            {'email': mock_form.cleaned_data.get('email')}
        )

    @patch('user.views.render')
    def test_renders_password_reset_with_form_if_form_invalid(
        self, mock_render, mockPasswordResetForm
    ):
        mock_form = mockPasswordResetForm.return_value
        mock_form.is_valid.return_value = False

        response = password_reset(self.request)

        self.assertEqual(response, mock_render.return_value)
        mock_render.assert_called_once_with(
            self.request,
            'registration/password_reset_form.html',
            {'form': mock_form}
        )


class InformationsViewUnitTest(TestCase):

    def setUp(self):
        self.request = HttpRequest()
        self.new_user = Profile.objects.create_user(
            'django@test.test',
            'django@test.test',
            'Django4321'
        )
        self.new_user.is_active = True
        self.new_user.signup_confirmation = True
        self.new_user.save()
        self.request.user = self.new_user

    @patch('user.views.render')
    def test_returns_render_with_args(
        self, mock_render
    ):
        response = informations(self.request)
        self.assertEqual(response, mock_render.return_value)
        mock_render.assert_called_once_with(
            self.request,
            'user/informations.html',
            {
                'user_uid':
                    urlsafe_base64_encode(force_bytes(self.new_user.pk)),
                'user_token':
                    account_activation_token.make_token(self.new_user),
                'roles': list(self.new_user.roles.all())
            }
        )


class AdminViewIntegratedTest(TestCase):

    def setUp(self):
        self.request = HttpRequest()
        self.request.user = _create_user_with_roles(Role.ADMIN)

    def test_uses_admin_template(self):
        self.client.force_login(self.request.user)
        response = self.client.get('/auth/admin')
        self.assertTemplateUsed(response, 'admin/admin.html')

    @patch('user.views.render')
    def test_returns_render_with_args(
        self, mock_render
    ):
        response = admin(self.request)
        self.assertEqual(response, mock_render.return_value)
        mock_render.assert_called_once_with(
            self.request,
            'admin/admin.html',
            {
                'users': list(Profile.objects.all())
            }
        )


@patch('user.views.EditUserForm')
class EditUserUnitTest(TestCase):

    def setUp(self):
        self.new_user = _create_user_with_roles(Role.ADMIN)
        self.request = HttpRequest()
        self.request.user = self.new_user
        self.request.POST['email'] = 'edith-new-email@example.com'
        self.request.POST['roles'] = [2, 7]

    def test_call_form_save_if_form_valid(self, mockEditUserForm):
        self.request.method = 'POST'
        mock_form = mockEditUserForm.return_value
        mock_form.is_valid.return_value = True
        edit_user(self.request, self.new_user.id)
        mock_form.save.assert_called_once()

    def test_passes_POST_data_to_EditUserForm(
        self, mockEditUserForm
    ):
        self.request.method = 'POST'
        edit_user(self.request, self.new_user.id)
        mockEditUserForm.assert_called_once_with(
            data=self.request.POST,
            instance=self.new_user
        )

    @patch('user.views.redirect')
    def test_redirect_to_admin_if_form_valid(
        self, mock_redirect, mockEditUserForm
    ):
        self.request.method = 'POST'
        mock_form = mockEditUserForm.return_value
        mock_form.is_valid.return_value = True

        response = edit_user(self.request, self.new_user.id)

        self.assertEqual(response, mock_redirect.return_value)
        mock_redirect.assert_called_once_with('/auth/admin')

    @patch('user.views.render')
    def test_renders_password_reset_with_form_if_form_invalid(
        self, mock_render, mockEditUserForm
    ):
        mock_form = mockEditUserForm.return_value
        mock_form.is_valid.return_value = False

        response = edit_user(self.request, self.new_user.id)

        self.assertEqual(response, mock_render.return_value)
        mock_render.assert_called_once_with(
            self.request,
            'admin/edit-user.html',
            {'user': self.new_user, 'form': mock_form}
        )
