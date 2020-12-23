
from django.urls import include, path
from rest_framework import routers
from . import views
from .views import (GroupList, FarmerProfileList, CreateFarmerProfile, UpdateFarmerProfile,FarmerProfileViewSet
,CreateFarmerGroup,FarmerProfileDetailView, EditFarmerGroup)
from rest_framework.urlpatterns import format_suffix_patterns



router = routers.DefaultRouter()
router.register(r'groups', views.GroupViewSet)
router.register(r'farmerprofiles', views.FarmerProfileViewSet, basename='FarmerProfile')

approve_farmer= FarmerProfileViewSet.as_view({
    'patch': 'approved',
    'get': 'retrieve',
    'put': 'decline',
    'delete': 'destroy',
    'get':'list',
    'post':'create'

})
# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.

app_name = 'farmer'
urlpatterns = [
    path('api/', include(router.urls)),
    path('groups', GroupList.as_view(), name='group_list'),
    path('create/group', CreateFarmerGroup.as_view(), name="create_farmer_group"),
    path('group/<int:pk>/edit', EditFarmerGroup.as_view(), name="edit_farmer_group"),
    path('farmerprofile', FarmerProfileList.as_view(), name='farmerprofile_list'),
    path('create/profile', CreateFarmerProfile.as_view(), name="create_farmer"),
    path('<int:pk>/edit/', UpdateFarmerProfile.as_view(), name="edit_farmer_profile"),
    path('<int:pk>/approve/', approve_farmer, name='approve'),

    path('<int:pk>/view/', FarmerProfileDetailView.as_view(), name="view_farmer_profile"),

    path('columnchart/', views.farmer_class_view, name ="column_chart")

]
