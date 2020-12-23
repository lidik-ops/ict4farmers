from django.urls import include, path
from rest_framework import routers
from . import views
from .views import CommunityWeatherList , ReportWeatherView, EditweatherView


router = routers.DefaultRouter()
router.register(r'community_weather', views.CommunityWeatherViewSet, 'community_weather')
router.register(r'community_weather_list', views.PostWeatherViewSet, 'list_community_weather')

app_name = 'weather'
urlpatterns = [
    path('api/', include(router.urls)),
    path('communityweather', CommunityWeatherList.as_view(), name='communityweather_list'),
    path('report/weather', ReportWeatherView.as_view(), name='report_weather'),
    path('<int:pk>/edit/', EditweatherView.as_view(), name="edit_weather"),
]
