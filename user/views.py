from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str

from user.forms import SignupForm, SigninForm
from django.contrib.auth.models import User
from user.tokens import account_activation_token

import logging

logger = logging.getLogger(__name__)

ACCOUNT_ACTIVATION_EMAIL_SUBJECT = 'Veuillez activer votre compte'


def signup(request):
    form = SignupForm(data=request.POST)
    if form.is_valid():
        email = form.cleaned_data.get('email')
        password = form.cleaned_data.get('password1')
        user = User.objects.create_user(email, email, password)
        # user can't login until link confirmed
        user.is_active = False
        user.save()
        current_site = get_current_site(request)
        subject = ACCOUNT_ACTIVATION_EMAIL_SUBJECT
        message = render_to_string('user/activation_request.html', {
            'user': user,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': account_activation_token.make_token(user),
        })
        user.email_user(subject, message)
        return redirect('/auth/sent')
    else:
        return render(request, 'user/signup.html', {
            'form': form
        })


def activation_sent(request):
    return render(request, 'user/activation_sent.html')


def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    # checking if the user exists, if the token is valid.
    if user is not None and account_activation_token.check_token(user, token):
        # if valid set active true
        user.is_active = True
        # set signup_confirmation true
        user.profile.signup_confirmation = True
        user.save()
        login(request, user)
        return redirect('/')
    else:
        return render(request, 'user/activation_invalid.html')


def signin(request):
    auth_error = False
    form = SigninForm(data=request.POST)
    if form.is_valid():
        email = form.cleaned_data.get('email')
        password = form.cleaned_data.get('password')
        user = authenticate(username=email, password=password)
        if user is not None and user.is_active:
            login(request, user)
            return redirect('/')
        else:
            auth_error = True

    return render(request, 'user/signin.html', {
        'form': form,
        'authentication_error': auth_error
    })


def signout(request):
    logout(request)
    return redirect('/')
