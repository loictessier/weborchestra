from django.shortcuts import render, redirect

from music_library.forms import ScoreForm, InstrumentForm, StandForm
from music_library.models import MusicScore, Instrument, Stand


def music_library(request):
    music_scores = MusicScore.objects.all()
    return render(request, 'music_library/music_library.html', {'music_scores': music_scores})


def new_score(request):
    form = ScoreForm(data=request.POST)
    if form.is_valid():
        score = form.save()
        return redirect(str(score.get_absolute_url()))
    return render(request, 'music_library/new_score.html', {'form': form})


def view_score(request, score_id):
    score = MusicScore.objects.get(id=score_id)
    instruments = Instrument.objects.filter(music_score=score)
    return render(request, 'music_library/score.html', {'score': score, 'instruments': instruments})


def new_instrument(request, score_id):
    form = InstrumentForm(data=request.POST)
    if form.is_valid():
        music_score = MusicScore.objects.get(id=score_id)
        instrument = form.save(music_score)
        return redirect(str(instrument.get_absolute_url()))
    return render(request, 'music_library/new_instrument.html', {'form': form})


def view_instrument(request, score_id, instrument_id):
    score = MusicScore.objects.get(id=score_id)
    instrument = Instrument.objects.get(id=instrument_id)
    stands = Stand.objects.filter(instrument=instrument)
    return render(request,
                  'music_library/instrument.html',
                  {'score': score, 'instrument': instrument, 'stands': stands})


def new_stand(request, score_id, instrument_id):
    form = StandForm(data=request.POST, files=request.FILES)
    if form.is_valid():
        instrument = Instrument.objects.get(id=instrument_id)
        stand = form.save(instrument)
        return redirect(str(stand.get_absolute_url()))
    return render(request, 'music_library/new_stand.html', {'form': form})


def view_stand(request, score_id, instrument_id, stand_id):
    score = MusicScore.objects.get(id=score_id)
    instrument = Instrument.objects.get(id=instrument_id)
    stand = Stand.objects.get(id=stand_id)
    return render(request, 'music_library/stand.html', {'score': score, 'instrument': instrument, 'stand': stand})
