"""ict4farmers URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from common .views import LoginView, LogoutView
from django.conf.urls.static import static
from django.conf import settings
from common.views import obtain_auth_token 
from rest_framework_swagger.views import get_swagger_view
schema_view = get_swagger_view(title="ICT4Farmers API Docs")

urlpatterns = [
    path('admin/', admin.site.urls),
    # api documentation
    path('api/docs', schema_view),
    # authentication urls
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    # api authentication urls
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('api-token-auth/', obtain_auth_token, name='api_token_auth'),

    # common urls
    path('', include('common.urls', namespace="common")),

    # open market urls
    path('api-openmarket/', include('openmarket.urls', namespace="api-openmarket")),
    path('openmarket/', include('openmarket.urls', namespace="openmarket")),

    # farm urls
  
    path('farm/', include('farm.urls', namespace="farm")),

    # farmer urls
   
    path('farmer/', include('farmer.urls', namespace="farmer")),

    # unffeagents urls
    path('api-unffeagents/', include('unffeagents.urls', namespace="api-unffeagents")),
    path('unffeagents/', include('unffeagents.urls', namespace="unffeagents")),

    # open weather urls
    path('api-weather/', include('weather.urls', namespace="api-weather")),
    path('weather/', include('weather.urls', namespace="weather")),

    # resorce sharing urls
    path('api-resourcesharing/', include('resourcesharing.urls', namespace="api-resourcesharing")),
    path('resourcesharing/', include('resourcesharing.urls', namespace="resourcesharing")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)