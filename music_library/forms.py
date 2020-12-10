from django import forms

from .models import MusicScore


class ScoreForm(forms.models.ModelForm):

    class Meta:
        model = MusicScore
        fields = ('name', 'author', 'editor',)
        widgets = {
            'name': forms.fields.TextInput(attrs={
                'placeholder': 'Nom de la partition'
            }),
            'author': forms.fields.TextInput(attrs={
                'placeholder': "Nom de l'auteur"
            }),
            'editor': forms.fields.TextInput(attrs={
                'placeholder': "Nom de l'éditeur"
            }),
        }


class NewScoreForm(ScoreForm):

    def save(self):
        return MusicScore.create_new(
            name=self.cleaned_data['name'],
            author=self.cleaned_data['author'],
            editor=self.cleaned_data['editor']
        )
