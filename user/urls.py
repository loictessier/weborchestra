from django.urls import path
from django.contrib.auth import views as auth_views

from . import views

app_name = 'user'

urlpatterns = [
    path('signup', views.signup, name='signup'),
    path('sent', views.activation_sent, name='activation_sent'),
    path('activate/<slug:uidb64>/<slug:token>/', views.activate, name='activate'),
    path('signin', views.signin, name='signin'),
    path('signout', views.signout, name='signout'),
    path('password_reset', views.password_reset, name='password_reset'),
    path('reset/<uidb64>/<token>/', views.PasswordResetConfirm.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('informations', views.informations, name='informations'),
    path('admin', views.admin, name='admin'),
    path('admin/<id>', views.edit_user, name='edit_user'),
]
