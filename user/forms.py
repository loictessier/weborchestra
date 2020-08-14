from django import forms

EMPTY_EMAIL_ERROR = "Vous ne pouvez pas avoir un champ email vide."

class SignupForm(forms.Form):
    email = forms.EmailField(
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