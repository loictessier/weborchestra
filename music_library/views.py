from django.shortcuts import render, redirect

from music_library.forms import NewScoreForm
from music_library.models import MusicScore


def music_library(request):
    music_scores = MusicScore.objects.all()
    return render(request, 'music_library/music_library.html', {'music_scores': music_scores})


def new_score(request):
    form = NewScoreForm(data=request.POST)
    if form.is_valid():
        score = form.save()
        return redirect(str(score.get_absolute_url()))
    return render(request, 'music_library/new_score.html', {'form': form})


def view_score(request, score_id):
    score = MusicScore.objects.get(id=score_id)
    return render(request, 'music_library/score.html', {'score': score})
