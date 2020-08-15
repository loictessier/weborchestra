from django.shortcuts import render, redirect
from django.http import HttpResponse

from user.forms import SignupForm
from user.models import Profile
from django.contrib.auth.models import User

# Create your views here.
def signup(request):
    if request.method == 'POST':
        new_email = request.POST['email']
        user = User.objects.create_user(new_email, new_email, 'test')
        profile = Profile(user=user)
        profile.save()
        return redirect('/')

    return render(request, 'user/signup.html', {
        'form': SignupForm()
    })
    