from django.urls import path

from . import views

app_name = 'music_library'

urlpatterns = [
    path('', views.music_library, name='music_library')
]
