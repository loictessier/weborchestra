from django.shortcuts import render
from django.http import HttpResponse

from user.forms import SignupForm
from user.models import Profile

# Create your views here.
def signup(request):
    return render(request, 'user/signup.html', {
        'form': SignupForm(), 
        'new_email': request.POST.get('email', '')
    })
    