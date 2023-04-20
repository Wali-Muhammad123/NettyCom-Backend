from django.shortcuts import render
from django.urls import reverse
from django.core.exceptions import ObjectDoesNotExist
from django.db.utils import IntegrityError
from rest_framework import generics, views, viewsets
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from .models import Directories, Teams, SalesData, TeamMembers
from .serializers import TeamSerializer, SaleSerializer,UserSerializer, _SaleSerializer
from .utilclasses import FakeNameGen
from .permissions import IsTeamLead
from .paginators import TeamSalesPaginater
from .utilfunc import _saleRetriever
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
                "teamleader":request.user.uuid,
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

class SaleView(generics.GenericAPIView):
    authentication_classes=[TokenAuthentication]
    permission_classes=[IsAuthenticated]
    throttle_scope='sales'
    serializer_class=SaleSerializer
    def get(self,request):
        # Get all sales of a user code
        queryset=SalesData.objects.filter(agent=request.user.uuid)
        serializer=SaleSerializer(queryset,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)
    def post(self,request, *args,**kwargs):
        #create a sale for a user as per the sale model
        serializer=self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data,status=status.HTTP_201_CREATED)
    def put(self,request):
        #update a sale for a user as per the sale model
        serializer=self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data,status=status.HTTP_200_OK)

class TeamSales(viewsets.ViewSet):
    authentication_classes=[TokenAuthentication]
    permission_classes=[IsAuthenticated, IsTeamLead]
    serializer_class=TeamSerializer
    pagination_class=TeamSalesPaginater
    def list(self,request):
        try:
            json_data={}
            teamId=Teams.objects.get(teamleader=request.user.uuid)
            queryset=TeamMembers.objects.get_queryset(team=teamId)
            if queryset is None:
                raise ObjectDoesNotExist
            serializer=UserSerializer(queryset,many=True)
            for member in serializer.data:
                json_data[member.uuid]={
                    "agentName":member.name,
                    "salesBooked":_saleRetriever(member.uuid),    
                }
            return Response(data=json_data,status=status.HTTP_302_FOUND)
        except ObjectDoesNotExist as exc:
            pass
    def retrieve(self,request,uuid=None):
        try:
            queryset=SalesData.objects.get_queryset(agent=uuid)
            if queryset is None:
                return Response({"msg":"No Sales Found"},status=status.HTTP_404_NOT_FOUND)
            else:
                serializer=_SaleSerializer(queryset,many=True)
                return Response(serializer.data,status=status.HTTP_200_OK)
        except ObjectDoesNotExist:
            ...

