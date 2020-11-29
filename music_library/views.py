from django.shortcuts import render


def music_library(request):
    return render(request, 'music_library/music_library.html')
