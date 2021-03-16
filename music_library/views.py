from django.shortcuts import render, redirect
from django.contrib.auth.decorators import user_passes_test, login_required

from music_library.forms import ScoreForm, InstrumentForm, StandForm
from music_library.models import MusicScore, Instrument, Stand
from user.models import Role


# custom decorator for role required
def role_required(*roles, login_url='/'):
    return user_passes_test(
        lambda u: u.has_any_role(roles), login_url=login_url)


def music_library(request):
    music_scores = MusicScore.objects.all()
    return render(
        request,
        'music_library/music_library.html',
        {'music_scores': music_scores})


# Test of decorators
@login_required(login_url='/auth/signin')
@role_required(Role.ADMIN,
               Role.MUSIC_LIBRARY_MODERATOR,
               login_url='/music-library')
def new_score(request):
    form = ScoreForm(data=request.POST)
    if form.is_valid():
        score = form.save()
        return redirect(str(score.get_absolute_url()))
    return render(request, 'music_library/new_score.html', {'form': form})


def view_score(request, score_id):
    score = MusicScore.objects.get(id=score_id)
    instruments = Instrument.objects.filter(music_score=score)
    return render(
        request,
        'music_library/score.html',
        {'score': score, 'instruments': instruments})


def new_instrument(request, score_id):
    music_score = MusicScore.objects.get(id=score_id)
    form = InstrumentForm(music_score=music_score, data=request.POST)
    if form.is_valid():
        instrument = form.save()
        return redirect(str(instrument.get_absolute_url()))
    return render(
        request,
        'music_library/new_instrument.html',
        {'form': form})


def view_instrument(request, score_id, instrument_id):
    score = MusicScore.objects.get(id=score_id)
    instrument = Instrument.objects.get(id=instrument_id)
    stands = Stand.objects.filter(instrument=instrument)
    return render(request,
                  'music_library/instrument.html',
                  {'score': score, 'instrument': instrument, 'stands': stands})


def new_stand(request, score_id, instrument_id):
    instrument = Instrument.objects.get(id=instrument_id)
    form = StandForm(
        instrument=instrument,
        data=request.POST,
        files=request.FILES
    )
    if form.is_valid():
        stand = form.save()
        return redirect(str(stand.get_absolute_url()))
    return render(request, 'music_library/new_stand.html', {'form': form})


def view_stand(request, score_id, instrument_id, stand_id):
    score = MusicScore.objects.get(id=score_id)
    instrument = Instrument.objects.get(id=instrument_id)
    stand = Stand.objects.get(id=stand_id)
    return render(
        request,
        'music_library/stand.html',
        {'score': score, 'instrument': instrument, 'stand': stand})
