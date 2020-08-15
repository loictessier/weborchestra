from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import login, authenticate

from user.forms import SignupForm
from user.models import Profile
from django.contrib.auth.models import User

# Create your views here.
def signup(request):
    form = SignupForm(data=request.POST)
    if form.is_valid():
        email = form.cleaned_data.get('email')
        password = form.cleaned_data.get('password1')
        user = User.objects.create_user(email, email, password)
        profile = Profile(user=user)
        profile.save()
        user = authenticate(username=email, password=password)
        login(request, user)
        return redirect('/')
    else:
        return render(request, 'user/signup.html', {
            'form': form
        })
    