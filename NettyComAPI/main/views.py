from django.shortcuts import render
from django.urls import reverse
from authemail.views import EmailVerificationView
# Create your views here.
def index(request):
    return render(request,{'title':'NettyCom'})
