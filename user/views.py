from django.shortcuts import render

from user.forms import SignupForm
from user.models import Profile

# Create your views here.
def signup(request):
    return render(request, 'user/signup.html', {'form': SignupForm()})