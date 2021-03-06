from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from music_library.forms import ScoreForm, InstrumentForm, StandForm
from music_library.models import MusicScore, Instrument, Stand
from user.models import Role
from user.decorators import role_required


@login_required(login_url='/auth/signin')
@role_required(Role.ADMIN,
               Role.MUSIC_LIBRARY_MODERATOR,
               Role.MUSICIAN,
               login_url='/')
def music_library(request):
    music_scores = MusicScore.objects.all()
    return render(
        request,
        'music_library/music_library.html',
        {'music_scores': music_scores})


@login_required(login_url='/auth/signin')
@role_required(Role.ADMIN,
               Role.MUSIC_LIBRARY_MODERATOR,
               login_url='/')
def new_score(request):
    form = ScoreForm(data=request.POST)
    if form.is_valid():
        score = form.save()
        return redirect(str(score.get_absolute_url()))
    return render(request, 'music_library/new_score.html', {'form': form})


@login_required(login_url='/auth/signin')
@role_required(Role.ADMIN,
               Role.MUSIC_LIBRARY_MODERATOR,
               Role.MUSICIAN,
               login_url='/')
def view_score(request, score_id):
    score = MusicScore.objects.get(id=score_id)
    instruments = Instrument.objects.filter(music_score=score)
    return render(
        request,
        'music_library/score.html',
        {'score': score, 'instruments': instruments})


@login_required(login_url='/auth/signin')
@role_required(Role.ADMIN,
               Role.MUSIC_LIBRARY_MODERATOR,
               login_url='/')
def delete_score(request, score_id):
    score = MusicScore.objects.get(id=score_id)
    score.delete()
    return redirect('/music-library')


@login_required(login_url='/auth/signin')
@role_required(Role.ADMIN,
               Role.MUSIC_LIBRARY_MODERATOR,
               login_url='/')
def edit_score(request, score_id):
    score = MusicScore.objects.get(id=score_id)
    if request.method == 'POST':
        form = ScoreForm(data=request.POST, instance=score)
        if form.is_valid():
            score = form.save(score.id)
            return redirect(str(score.get_absolute_url()))
    else:
        form = ScoreForm(instance=score)
        return render(request, 'music_library/new_score.html', {'form': form})


@login_required(login_url='/auth/signin')
@role_required(Role.ADMIN,
               Role.MUSIC_LIBRARY_MODERATOR,
               login_url='/')
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


@login_required(login_url='/auth/signin')
@role_required(Role.ADMIN,
               Role.MUSIC_LIBRARY_MODERATOR,
               Role.MUSICIAN,
               login_url='/')
def view_instrument(request, score_id, instrument_id):
    score = MusicScore.objects.get(id=score_id)
    instrument = Instrument.objects.get(id=instrument_id)
    stands = Stand.objects.filter(instrument=instrument)
    return render(request,
                  'music_library/instrument.html',
                  {'score': score, 'instrument': instrument, 'stands': stands})


@login_required(login_url='/auth/signin')
@role_required(Role.ADMIN,
               Role.MUSIC_LIBRARY_MODERATOR,
               login_url='/')
def delete_instrument(request, score_id, instrument_id):
    score = MusicScore.objects.get(id=score_id)
    instrument = Instrument.objects.get(id=instrument_id)
    instrument.delete()
    return redirect(str(score.get_absolute_url()))


@login_required(login_url='/auth/signin')
@role_required(Role.ADMIN,
               Role.MUSIC_LIBRARY_MODERATOR,
               login_url='/')
def edit_instrument(request, score_id, instrument_id):
    score = MusicScore.objects.get(id=score_id)
    instrument = Instrument.objects.get(id=instrument_id)
    if request.method == 'POST':
        form = InstrumentForm(
            music_score=score,
            data=request.POST,
            instance=instrument
        )
        if form.is_valid():
            instrument = form.save(instrument.id)
            return redirect(str(instrument.get_absolute_url()))
    else:
        form = InstrumentForm(music_score=score, instance=instrument)
        return render(
            request,
            'music_library/new_instrument.html',
            {'form': form}
        )


@login_required(login_url='/auth/signin')
@role_required(Role.ADMIN,
               Role.MUSIC_LIBRARY_MODERATOR,
               login_url='/')
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


@login_required(login_url='/auth/signin')
@role_required(Role.ADMIN,
               Role.MUSIC_LIBRARY_MODERATOR,
               Role.MUSICIAN,
               login_url='/')
def view_stand(request, score_id, instrument_id, stand_id):
    score = MusicScore.objects.get(id=score_id)
    instrument = Instrument.objects.get(id=instrument_id)
    stand = Stand.objects.get(id=stand_id)
    return render(
        request,
        'music_library/stand.html',
        {'score': score, 'instrument': instrument, 'stand': stand})


@login_required(login_url='/auth/signin')
@role_required(Role.ADMIN,
               Role.MUSIC_LIBRARY_MODERATOR,
               login_url='/')
def delete_stand(request, score_id, instrument_id, stand_id):
    instrument = Instrument.objects.get(id=instrument_id)
    stand = Stand.objects.get(id=stand_id)
    stand.delete()
    return redirect(str(instrument.get_absolute_url()))


@login_required(login_url='/auth/signin')
@role_required(Role.ADMIN,
               Role.MUSIC_LIBRARY_MODERATOR,
               login_url='/')
def edit_stand(request, score_id, instrument_id, stand_id):
    instrument = Instrument.objects.get(id=instrument_id)
    stand = Stand.objects.get(id=stand_id)
    if request.method == 'POST':
        form = StandForm(
            instrument=instrument,
            data=request.POST,
            files=request.FILES,
            instance=stand
        )
        if form.is_valid():
            stand = form.save(stand.id)
            return redirect(str(stand.get_absolute_url()))
    else:
        form = StandForm(
            instrument=instrument,
            instance=stand
        )
    return render(
        request,
        'music_library/new_stand.html',
        {'form': form}
    )
