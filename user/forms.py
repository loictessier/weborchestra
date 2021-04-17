from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django import forms
from django.contrib.auth.forms import (
    UserCreationForm, AuthenticationForm,
    PasswordResetForm, SetPasswordForm
)

from user.tokens import account_activation_token
from user.models import Profile, Role

EMPTY_EMAIL_ERROR = "Vous ne pouvez pas avoir un champ email vide."
DUPLICATE_USER_ERROR = (
    "Un utilisateur correspondant à cette adresse email existe déjà."
)


class SignupForm(UserCreationForm):
    email = forms.EmailField(
        max_length=200,
        widget=forms.TextInput(
            attrs={
                'type': 'email',
                'placeholder': 'exemple@adresse.com',
                'class': 'form-control input-lg'
            }
        ),
        error_messages={
            'required': EMPTY_EMAIL_ERROR
        }
    )

    def save(
        self, request,
        subject_template_name='registration/activation_request_subject.txt',
        email_template_name='registration/activation_request_email.html'
    ):
        email = self.cleaned_data['email']
        users = self.get_users(email)
        current_site = get_current_site(request)
        if users.exists() and not users[0].is_active:
            self.send_confirm_email(
                users[0],
                current_site,
                subject_template_name,
                email_template_name)
            return users[0]
        else:
            email = self.cleaned_data.get('email')
            password = self.cleaned_data.get('password1')
            user = Profile.objects.create_user(email, email, password)
            # user can't login until link confirmed
            user.is_active = False
            user.save()
            self.send_confirm_email(
                user,
                current_site,
                subject_template_name,
                email_template_name)
            return user

    def clean_email(self):
        email = self.cleaned_data['email']
        users = self.get_users(email)
        if users.exists() and users[0].is_active:
            raise forms.ValidationError(
                self.error_messages['email_duplicate']
            )
        return email

    def get_users(self, email):
        return Profile.objects.exclude(
            pk=self.instance.pk).filter(username=email)

    def send_confirm_email(self, user, current_site,
                           subject_template_name, email_template_name):
        subject = render_to_string(
            subject_template_name,
            {'site_name': current_site.name}
        )
        message = render_to_string(email_template_name, {
            'user': user,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': account_activation_token.make_token(user),
        })
        user.email_user(subject, message)

    def __init__(self, *args, **kwargs):
        super(SignupForm, self).__init__(*args, **kwargs)
        self.fields['password1'].widget.attrs['placeholder'] = '********'
        self.fields['password2'].widget.attrs['placeholder'] = '********'
        self.error_messages['email_duplicate'] = DUPLICATE_USER_ERROR

    class Meta:
        model = Profile
        fields = ('email', 'password1', 'password2')


class SigninForm(AuthenticationForm):
    email = forms.EmailField(
        max_length=200,
        widget=forms.TextInput(
            attrs={
                'type': 'email',
                'placeholder': 'exemple@adresse.com',
                'class': 'form-control input-lg'
            }
        ),
        error_messages={
            'required': EMPTY_EMAIL_ERROR
        }
    )
    field_order = ['email', 'password']

    def __init__(self, *args, **kwargs):
        super(SigninForm, self).__init__(*args, **kwargs)
        self.fields.pop('username')
        self.fields['password'].widget.attrs['placeholder'] = '********'

    class Meta:
        model = Profile
        fields = ('email', 'password')


class PasswordResetForm(PasswordResetForm):
    email = forms.EmailField(
        max_length=200,
        widget=forms.EmailInput(
            attrs={
                'placeholder': 'exemple@adresse.com',
                'class': 'form-control input-lg'
            }
        ),
        error_messages={
            'required': EMPTY_EMAIL_ERROR
        }
    )


class SetPasswordForm(SetPasswordForm):

    def __init__(self, user, *args, **kwargs):
        super(SetPasswordForm, self).__init__(user, *args, **kwargs)
        self.fields['new_password1'].widget.attrs['placeholder'] = '********'
        self.fields['new_password2'].widget.attrs['placeholder'] = '********'


class EditUserForm(forms.ModelForm):
    email = forms.EmailField(label='Adresse mail', max_length=200)
    roles = forms.ModelMultipleChoiceField(
        label='Rôles',
        queryset=Role.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    def save(self, user):
        super().save()
        user.username = self.cleaned_data['email']
        user.save()

    class Meta:
        model = Profile
        fields = ('email', 'roles')
