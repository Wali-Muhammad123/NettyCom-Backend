from rest_framework import serializers
from .models import SalesData, Agent, AddressCheckerUsage, Directories

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Agent
        fields = '__all__'

class SaleSerializer(serializers.ModelSerializer):
    class Meta:
        model = SalesData
        fields = '__all__'

class AddressCheckerSerializer(serializers.ModelSerializer):
    user=UserSerializer(read_only=True)
    class Meta:
        model = AddressCheckerUsage
        fields='__all__'
class DirectorySerializer(serializers.ModelSerializer):
    coordinates=serializers.ListField(child=serializers.FloatField(),allow_blank=False,max_length=2,min_length=2)
    class Meta:
        model=Directories
        fields='__all__'
   