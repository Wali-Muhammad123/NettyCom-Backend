from rest_framework import serializers
from django.conf import settings
from .models import SalesData, Agent, AddressCheckerUsage,Teams

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Agent
        fields = '__all__'

class SaleSerializer(serializers.ModelSerializer):
    class Meta:
        model = SalesData
        fields = '__all__'

class AddressCheckerSerializer(serializers.Serializer):
    user=serializers.PrimaryKeyRelatedField(queryset=Agent.objects.all())
    class Meta:
        model = AddressCheckerUsage
        fields='__all__'
    
class TeamSerializer(serializers.ModelSerializer):
    teamleader=serializers.PrimaryKeyRelatedField(queryset=Agent.objects.all())
    class Meta:
        model=Teams 
        fields='__all__'
    def create(self,  validated_data):
        team=Teams.objects.create(**validated_data)
        return team
    def update(self, instance, validated_data):
        for key,value in validated_data.items():
            setattr(instance,key,value)
        instance.save()
        return instance
    
