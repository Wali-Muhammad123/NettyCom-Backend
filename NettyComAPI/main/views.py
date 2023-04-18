from django.shortcuts import render
from django.urls import reverse
from django.core.exceptions import ObjectDoesNotExist
from django.db.utils import IntegrityError
from rest_framework import generics, views
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from .models import Directories, Teams
from .serializers import TeamSerializer
from .utilclasses import FakeNameGen
# Create your views here.
def index(request):
    return render(request,{'title':'NettyCom'})

class TeamView(generics.GenericAPIView):
    authentication_classes=[TokenAuthentication]
    permission_classes=[IsAuthenticated]
    throttle_scope='createteam'
    serializer_class=TeamSerializer
    def get(self, request):
        try:
            json_data={
                "teamName":Teams.objects.get(teamleader=request.user.uuid).team_name,
                "teamleader":request.user.uuid
            }
        except ObjectDoesNotExist:
            return Response({"msg":"Team DoesNot Exist"},status=status.HTTP_404_NOT_FOUND)
    def post(self,request,*args,**kwargs):
        try:
            json_data={
                'team_name':FakeNameGen().random_selector(),
                'teamleader':request.user.uuid
            }
            serializer=self.get_serializer(data=json_data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        except IntegrityError:
            return Response({"msg":"Something went wrong. Try again or Try Again Later."},status=status.HTTP_400_BAD_REQUEST)
    def put(self,request, *args, **kwargs):
        try:
            title=request.data.get('team_name')
            if title is not None:
                instance=Teams.objects.get(uuid=request.user.uuid)
                serializer=TeamSerializer(instance=instance,data=request.data,partial=True)
                serializer.is_valid(raise_exception=True)
                return Response(serializer.data,status=status.HTTP_200_OK)
            else:
                new_name=FakeNameGen().random_selector()
                instance=Teams.objects.get(uuid=request.user.uuid)
                serializer=TeamSerializer(instance=instance,data={'team_name':new_name},partial=True)
                serializer.is_valid(raise_exception=True)
                return Response(serializer.data,status=status.HTTP_200_OK)
        except IntegrityError:
            return Response({"msg":"Something went wrong. Try again or Try Again Later."},status=status.HTTP_400_BAD_REQUEST)