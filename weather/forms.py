
from .models import CommunityWeather
from django.contrib.gis import forms 
from django.contrib.gis.geos import Point



class WeatherForm(forms.ModelForm):
    location = forms.PointField(widget=forms.OSMWidget(attrs={'map_width': 800, 'map_height': 500, 'mouse_position': True,'default_zoom':7}),
    initial=Point(y=1.0609637, x=32.5672804, srid=4326))

  
    class Meta:
        model = CommunityWeather
        exclude = ['date_reported','reported_by','time_reported']

    def __init__(self, *args, **kwargs):
        super(WeatherForm, self).__init__(*args, **kwargs)
        self.fields['description'].widget.attrs.update({'rows': '1'})

   