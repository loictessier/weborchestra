from django import forms

from .models import MusicScore, Instrument, Stand


class ScoreForm(forms.models.ModelForm):

    class Meta:
        model = MusicScore
        fields = ('name', 'author', 'editor',)
        widgets = {
            'name': forms.fields.TextInput(attrs={
                'placeholder': "Nom de la partition"
            }),
            'author': forms.fields.TextInput(attrs={
                'placeholder': "Nom de l'auteur"
            }),
            'editor': forms.fields.TextInput(attrs={
                'placeholder': "Nom de l'éditeur"
            }),
        }

    def save(self):
        return MusicScore.objects.create(
            name=self.cleaned_data['name'],
            author=self.cleaned_data['author'],
            editor=self.cleaned_data['editor']
        )


class InstrumentForm(forms.models.ModelForm):

    class Meta:
        model = Instrument
        fields = ('name',)
        widgets = {
            'name': forms.fields.TextInput(attrs={
                'placeholder': "Nom de l'instrument"
            })
        }

    def save(self, music_score):
        return Instrument.objects.create(
            name=self.cleaned_data['name'],
            music_score=music_score
        )


class StandForm(forms.models.ModelForm):

    class Meta:
        model = Stand
        fields = ('name', 'score',)
        widgets = {
            'name': forms.fields.TextInput(attrs={
                'placeholder': 'Nom du pupitre'
            })
        }

    def save(self, instrument):
        return Stand.objects.create(
            name=self.cleaned_data['name'],
            score=self.cleaned_data['score'],
            instrument=instrument
        )
