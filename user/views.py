import logging

from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.views import PasswordResetConfirmView
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_str, force_bytes
from django.urls import reverse_lazy

from user.forms import (
    SignupForm, SigninForm,
    PasswordResetForm, SetPasswordForm,
    EditUserForm
)
from user.tokens import account_activation_token
from user.models import Profile

logger = logging.getLogger(__name__)


def signup(request):
    form = SignupForm(data=request.POST)
    if form.is_valid():
        form.save(request=request)
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
        user = Profile.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, Profile.DoesNotExist):
        user = None
    # checking if the user exists, if the token is valid.
    if user is not None and account_activation_token.check_token(user, token):
        # if valid set active true
        user.is_active = True
        # set signup_confirmation true
        user.signup_confirmation = True
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


def password_reset(request):
    form = PasswordResetForm(data=request.POST)
    if form.is_valid():
        email = form.cleaned_data.get('email')
        form.save(
            use_https=request.is_secure(),
            from_email=None,
            subject_template_name='registration/password_reset_subject.txt',
            email_template_name='registration/password_reset_email.html',
            token_generator=account_activation_token,
            request=request)
        return render(
            request,
            'registration/password_reset_done.html',
            {'email': email})
    return render(
        request,
        'registration/password_reset_form.html',
        {'form': form})


class PasswordResetConfirm(PasswordResetConfirmView):
    form_class = SetPasswordForm
    post_reset_login = True
    success_url = reverse_lazy('user:password_reset_complete')
    token_generator = account_activation_token


def informations(request):
    uid = urlsafe_base64_encode(force_bytes(request.user.pk))
    token = account_activation_token.make_token(request.user)
    roles = request.user.roles.all()
    return render(
        request,
        'user/informations.html',
        {'user_uid': uid, 'user_token': token, 'roles': list(roles)})


def admin(request):
    users = Profile.objects.all()
    return render(request, 'admin/admin.html', {'users': list(users)})


def edit_user(request, id):
    user = Profile.objects.get(id=id)
    if request.method == 'POST':
        form = EditUserForm(data=request.POST, instance=user)
        if form.is_valid():
            form.save(user=user)
            return redirect('/auth/admin')
    else:
        form = EditUserForm(instance=user)
    return render(
        request,
        'admin/edit-user.html',
        {'user': user, 'form': form})
