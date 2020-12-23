from django.shortcuts import render
from .models import CommunityWeather
from .serializers import CommunityWeatherSerializer, PostWeatherSerializer
from rest_framework import viewsets
from django.contrib.auth.mixins import LoginRequiredMixin, AccessMixin
from rest_framework import permissions
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import filters
from django.contrib.gis.geos import fromstr
from django.contrib.gis.db.models.functions import Distance
from django.contrib.gis.geos import Point
from django.views.generic import (
    CreateView, UpdateView, DetailView, TemplateView, View, DeleteView)
from .forms import WeatherForm
from django.http import (HttpResponseRedirect,JsonResponse, HttpResponse,
                         Http404)
from django.shortcuts import redirect

#views for products
class CommunityWeatherViewSet(viewsets.ModelViewSet):
    """
    API endpoint to show weather on the dashboard, you pass in lon->longitude and lat->latitude.
    in the request e.g "/weather/api/community_weather/?lon=1.2345533&lat=32.5376262;
    """
    serializer_class = CommunityWeatherSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.SearchFilter,filters.OrderingFilter]
    search_fields = ['id','weather','reported_by__first_name','date_reported','time_reported','description','lon','lat']
    ordering_fields = '__all__'

    def get_queryset(self):
       
        #,'-id','-date_reported','time_reported'
        lon = float(self.request.query_params.get('lon', None))
        lat = float(self.request.query_params.get('lat', None))
        user_location = Point(lon, lat, srid=4326)
        queryset = CommunityWeather.objects.annotate(distance=Distance("location", user_location)).filter(distance__lte=1000).order_by('-date_reported','-time_reported','distance')[0:1]
        print(queryset)
        return queryset

    def create(self, request, format=None):
        serializer = PostWeatherSerializer(data=request.data)

        if serializer.is_valid():
            try:
                serializer.status ='active'
                user = self.request.user
                serializer.save(reported_by = user)
            except:
                return Response({'error':'Failed to save'})
                
            return Response({'status':'successful'})
        return Response(serializer.errors, status=400)


class CommunityWeatherList(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'communityweather_list.html'

    def get(self, request):
        queryset = CommunityWeather.objects.order_by('-id')
        return Response({'communityweathers': queryset})



class PostWeatherViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows products to be viewed or edited.
    """
    serializer_class = CommunityWeatherSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.SearchFilter,filters.OrderingFilter]
    search_fields = ['id','weather','reported_by__first_name','date_reported','time_reported','description','weather']
    ordering_fields = '__all__'

    def get_queryset(self):
        queryset = CommunityWeather.objects.all().order_by('-date_reported','-id')
        #print(queryset)
        return queryset

    def create(self, request, format=None):
        serializer = PostWeatherSerializer(data=request.data)

        if serializer.is_valid():
            try:
                user = self.request.user
                serializer.save(reported_by = user)
            except:
                return Response({'error':'Failed to save'})
                
            return Response({'status':'successful'})
        return Response(serializer.errors, status=400)

# report weather information from the browser
class ReportWeatherView(LoginRequiredMixin,CreateView):
    template_name = 'report_weather.html'
    form_class = WeatherForm
    success_message = "weather reported successfully"


    def dispatch(self, request, *args, **kwargs):
        return super(ReportWeatherView, self).dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super(ReportWeatherView, self).get_form_kwargs()
        return kwargs


    def post(self, request, *args, **kwargs):
        self.object = None
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            print(form.errors)
        return self.form_invalid(form)


    def form_valid(self, form):
        weather = form.save(commit=False)
        weather.reported_by = self.request.user
        weather.save()

        return redirect('weather:communityweather_list')

    def form_invalid(self, form):
        if self.request.is_ajax():
            return JsonResponse({'error': True, 'errors': form.errors})
        return self.render_to_response(self.get_context_data(form=form))

# update farm view
class EditweatherView(LoginRequiredMixin,UpdateView):
    model = CommunityWeather
    template_name = 'report_weather.html'
    form_class = WeatherForm
    success_message = "Weather info updated successfully"


    def dispatch(self, request, *args, **kwargs):
        return super(EditweatherView, self).dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super(EditweatherView, self).get_form_kwargs()
        return kwargs


    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            print(form.errors)
        return self.form_invalid(form)


    def form_valid(self, form):
        weather = form.save(commit=False)
        weather.save()
        return redirect('weather:communityweather_list')