from django.shortcuts import render
from django.core.mail import send_mail
from django.conf import settings


# Create your views here.
def index(request):
    return render(request, 'core/index.html')


def legal_notice(request):
    return render(request, 'core/legals.html')


def contact(request):
    send_mail(
        subject=request.POST['subject'],
        message=request.POST['message'],
        from_email=request.POST['email'],
        recipient_list=[settings.CONTACT_EMAIL]
    )
    return render(request, 'core/index.html')
