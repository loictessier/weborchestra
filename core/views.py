from django.shortcuts import render


# Create your views here.
def index(request):
    return render(request, 'core/index.html')


def legal_notice(request):
    return render(request, 'core/legals.html')
