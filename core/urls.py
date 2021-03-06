from django.urls import path

from . import views

app_name = 'core'

urlpatterns = [
    path('', views.index, name='index'),
    path('legals/', views.legal_notice, name='legals'),
    path('contact', views.contact, name='contact')
]
