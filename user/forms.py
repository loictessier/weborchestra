from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

EMPTY_EMAIL_ERROR = "Vous ne pouvez pas avoir un champ email vide."
DUPLICATE_USER_ERROR = "Un utilisateur correspondant à cette adresse email existe déjà."

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
            'required': EMPTY_EMAIL_ERROR
        }
    )
    
    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.exclude(pk=self.instance.pk).filter(username=email).exists():
            raise forms.ValidationError(
                self.error_messages['email_duplicate']
            )
        return email

    def __init__(self, *args, **kwargs):
        super(SignupForm, self).__init__(*args, **kwargs)
        self.fields['password1'].widget.attrs['placeholder'] = '********'
        self.fields['password2'].widget.attrs['placeholder'] = '********'
        self.error_messages['email_duplicate'] = DUPLICATE_USER_ERROR

    class Meta:
        model = User
        fields = ('email', 'password1', 'password2')
