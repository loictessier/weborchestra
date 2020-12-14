from django.urls import path

from . import views

app_name = 'music_library'

urlpatterns = [
    path('', views.music_library, name='music_library'),
    path('new-score', views.new_score, name='new_score'),
    path('<int:score_id>/', views.view_score, name='view_score'),
    path('<int:score_id>/new-instrument', views.new_instrument, name='new_instrument'),
    path('<int:score_id>/<int:instrument_id>/', views.view_instrument, name='view_instrument'),
    path('<int:score_id>/<int:instrument_id>/new-stand', views.new_stand, name='new_stand'),
    path('<int:score_id>/<int:instrument_id>/<int:stand_id>/', views.view_stand, name='view_stand'),
]
