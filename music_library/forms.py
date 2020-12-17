from django import forms

from .models import MusicScore, Instrument, Stand

DUPLICATE_INSTRUMENT_ERROR = (
    "Un instrument avec ce nom existe déjà pour cette partition"
)
DUPLICATE_STAND_ERROR = (
    "Un pupitre avec ce nom existe déjà pour cet instrument"
)


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

    def __init__(self, music_score, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.music_score = music_score

    def clean_name(self):
        name = self.cleaned_data.get('name')
        if self.music_score.instrument_set.filter(name=name).exists():
            raise forms.ValidationError(DUPLICATE_INSTRUMENT_ERROR)
        return name

    def save(self):
        return Instrument.objects.create(
            name=self.clean_name(),
            music_score=self.music_score
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

    def __init__(self, instrument, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.instrument = instrument

    def clean_name(self):
        name = self.cleaned_data.get('name')
        if self.instrument.stand_set.filter(name=name).exists():
            raise forms.ValidationError(DUPLICATE_STAND_ERROR)
        return name

    def save(self):
        return Stand.objects.create(
            name=self.clean_name(),
            score=self.cleaned_data['score'],
            instrument=self.instrument
        )
