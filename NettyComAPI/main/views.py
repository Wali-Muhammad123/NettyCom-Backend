from django.shortcuts import render
from django.urls import reverse
from rest_framework import generics, views, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.request import Request
from django.core.mail import send_mail
from django.core.exceptions import ValidationError
from .models import Directories, AddressCheckerUsage
from .serializers import DirectorySerializer
from .utilclasses import MatrixRouter
from .exceptions import NullQueryError
# Create your views here.
def index(request):
    return render(request,{'title':'NettyCom'})

class MapView(viewsets.ViewSet):
    authentication_classes=[TokenAuthentication,SessionAuthentication]
    throttle_scope='map'
    permission_classes=[IsAuthenticated]
    def list(self,request,*args,**kwargs):
        '''
        This method is used to list all the directories in the database
        '''
        queryset=Directories.objects.all()
        serializer=DirectorySerializer(queryset,many=True)
        return Response(serializer.data)
    def retrieve(self,request,pk=None):
        '''
        This method is used to retrieve a directory by its state.
        '''
        queryset=Directories.objects.get(state=request.data['state'],postal_code=request.data['postal_code'])
        if queryset is None:
            raise NullQueryError
        else:
            serializer=DirectorySerializer(queryset)
            return Response(serializer.data)
    @action(methods=['post','get'])
    def fsearch(self,request,*args,**kwargs):
        '''
        This method is used to perform a full search for the customer's location in the working state.
        '''
        MATRIXROUTER=MatrixRouter(**request.data)
        InRoute=MATRIXROUTER.fullsearch()
        serialized_data={
            'ourDir':DirectorySerializer(InRoute[0]).data,
            'customerDir':InRoute[1],
            'distance':InRoute[2],
        }
        try:
            usage=AddressCheckerUsage.objects.create(
                user=request.user.UUID,
                directory=InRoute[0].id,
                response={
                    "postal_code":InRoute[1][1],
                    "countrySecondaySubdivision":InRoute[1][2],
                    "countrySubdivision":InRoute[1][0]
                }
            )
            usage.save()
        except ValidationError:
            send_mail(
                subject='Error Occuring in Address Checker',
                message='Address Checker is not saving relevant data. This is may cause unnecessary usage of AddressChecker and is a potentiol threat to the business',
                recipient_list=['renedescartian@gmail.com'],
                from_email=None
            )
            
        return Response(serialized_data, status=200)


    

