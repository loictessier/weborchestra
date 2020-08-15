from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

EMPTY_EMAIL_ERROR = "Vous ne pouvez pas avoir un champ email vide."

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
        error_messages = {
            'required': EMPTY_EMAIL_ERROR,
        }
    )

    def __init__(self, *args, **kwargs):
        super(SignupForm, self).__init__(*args, **kwargs)
        self.fields['password1'].widget.attrs['placeholder'] = '********'
        self.fields['password2'].widget.attrs['placeholder'] = '********'

    class Meta:
        model = User
        fields = ('email', 'password1', 'password2')