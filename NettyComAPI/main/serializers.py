from rest_framework import serializers
from .models import SalesData, Agent, AddressCheckerUsage

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Agent
        fields = '__all__'

class SaleSerializer(serializers.ModelSerializer):
    class Meta:
        model = SalesData
        fields = '__all__'

class AddressCheckerSerializer(serializers.Serializers):
    user=UserSerializer(read_only=True)
    class Meta:
        model = AddressCheckerUsage
        fields='__all__'