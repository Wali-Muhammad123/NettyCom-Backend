from rest_framework import serializers
from .models import SalesData, Agent, AddressCheckerUsage, Directories
from jsonfield.encoder import JSONEncoder

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
    coordinates=serializers.JSONField(encoder=JSONEncoder)
    class Meta:
        model=Directories
        fields='__all__'
    def validate_coordinates(self,json_dict):
        if isinstance(json_dict,dict):
            raise serializers.ValidationError("Coordinates must be a dictionary")
        if 'lat' not in json_dict or 'lon' not in json_dict:
            raise serializers.ValidationError("Coordinates must have latitude and longitude")
        return json_dict
    
