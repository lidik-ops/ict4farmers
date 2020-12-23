from rest_framework import serializers
from .models import CommunityWeather
from django.contrib.auth.models import User
from common.customSerializers import GeometryPointFieldSerializerFields
from geopy.geocoders import Nominatim

class CommunityWeatherSerializer(serializers.ModelSerializer):
    icon = serializers.CharField(source='weather', read_only=True)
    weather = serializers.CharField(source='get_weather_display')
    village = serializers.CharField(source='compute_location',required=False, read_only=True)
    location = GeometryPointFieldSerializerFields()
    reported_by = serializers.SerializerMethodField(method_name='get_weather_agent',source='reported_by')
    date_reported = serializers.DateField(format='%d-%m-%Y', read_only=True)
    time_reported = serializers.TimeField(format='%I:%M %p', read_only=True)

    class Meta:
        model = CommunityWeather 
        fields = ['id','icon','weather','village','reported_by','date_reported','time_reported','description','location']
    

    def get_weather_agent(self, obj):
        return '{} {}'.format(obj.reported_by.first_name, obj.reported_by.last_name)
    
   

class PostWeatherSerializer(serializers.ModelSerializer):


    class Meta:
        model = CommunityWeather 
        fields = ['weather','description','location']
    
