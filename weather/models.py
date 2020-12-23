from django.db import models
from common .models import TimeStampedModel
from django.utils.translation import ugettext as _
from django.contrib.auth.models import User
from django.contrib.gis.db import models
from geopy.geocoders import Nominatim
from django.contrib.gis.db import models

# Create your models here.

class CommunityWeather(TimeStampedModel, models.Model):
    WEATHER_CHOICES=(
        (
        None, "--please select--"),
        ('01d','Sunshine'),
        ('02d','Few clouds'),
        ('03d','Scattered clouds'),
        ('04d','Broken clouds'),
        ('09d','Shower rain'),
        ('10d','Rain'),
        ('11d','Thunderstorm'),
        ('13d','Snow'),
        ('50d','Mist')
    )
    
    weather = models.CharField(max_length=50,choices=WEATHER_CHOICES, null=False, blank=False)
    date_reported = models.DateField(auto_now=True)
    time_reported = models.TimeField(auto_now=True)
    reported_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='weather_agent')
    description = models.TextField(null=False, blank=False)
    #location of person reporting weather
    location = models.PointField( srid=4326,null=True)
   
    def __str__(self):
        return self.weather

    @property
    def compute_location(self):
        geolocator = Nominatim(user_agent="ICT4Farmers", timeout=10)
        lat = str(self.location.y)
        lon = str(self.location.x)
       
        try:

            location = geolocator.reverse(lat + "," + lon)
            return '{}'.format(location.address)
        except:
            location = str(self.location.y) + "," + str(self.location.x)
            return 'slow network, loading location ...'