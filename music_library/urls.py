from django.urls import path

from . import views

app_name = 'music_library'

urlpatterns = [
    path('', views.music_library, name='music_library'),
    path('new-score', views.new_score, name='new_score'),
    path('<int:score_id>/', views.view_score, name='view_score'),
]
