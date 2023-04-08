from django.shortcuts import render
from django.urls import reverse
from rest_framework import generics, views
from .models import Directories
# Create your views here.
def index(request):
    return render(request,{'title':'NettyCom'})

class AddressCheckerView(views.APIView):
    authentication_classes=[TokenAuthenticated]
    permission_classes=[IsAuthenticated]
    throttle_scope='addresschecker'
    serializer_class=AddressCheckerSerializer
    def get(self, request):
        pass
    def post(self, request):
        pass 
