from django.contrib import admin

# Register your models here.
from django.contrib.gis.admin import OSMGeoAdmin
from .models import CommunityWeather
@admin.register(CommunityWeather)

class WeatherAdmin(OSMGeoAdmin):
    list_display = [
        'weather',
        'reported_by',
        'description',
        'location',
        ]
