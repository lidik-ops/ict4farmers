from django.urls import include, path
from rest_framework import routers
from . import views
from .views import (ProductList,
                    SellerList,
                    CreateSellerProfile,
                    CreateProductProfile,
                    BuyerList,
                    ServiceProviderList,
                    ServiceRegistrationList,
                    SellerPostList,
                    BuyerPostList,
                    ContactDetailsList,
                    LogiticsList,
                    SellerViewSet,
                    # PackagingList,
                    # MedicalList,
                    SoilScienceList,
                    ServiceProviderProfileList,
                    CreateServiceProviderProfile,
                    load_districts,
                    CreateServiceView,
                    ServiceProviderViewSet,
                    UpdateServiceProviderProfile,
                    ServiceProviderProfileDetailView,
                    ServiceDetailView,
                    MapServiceDetailView,
                    EditServiceView
                     )

router = routers.DefaultRouter()
router.register(r'products', views.ProductViewSet)
router.register(r'categories', views.CategoryViewSet)
router.register(r'sellers', views.SellerViewSet)
router.register(r'buyers', views.BuyerViewSet)
router.register(r'sellerposts', views.SellerPostViewSet)
router.register(r'buyersposts', views.BuyerPostViewSet)
router.register(r'serviceproviders', views.ServiceProviderViewSet, basename='service_providers')

router.register(r'serviceregistration', views.ServiceRegistrationViewSet,  basename='services')

router.register(r'contactdetails', views.ContactDetailsViewSet)
router.register(r'logistics', views.LogisticsViewSet)
router.register(r'soilsciences', views.SoilScienceViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API
# 

approve_serviceprovider= ServiceProviderViewSet.as_view({
    'patch': 'approved',
    'get': 'retrieve',
    'put': 'decline',
    'delete': 'destroy',
    'get':'list'})

approve_seller= SellerViewSet.as_view({
    'patch': 'approved',
    'get': 'retrieve',
    'put': 'decline',
    'delete': 'destroy',
    'get':'list',
    'post':'create'

})

app_name = 'openmarket'

urlpatterns = [
    path('api/', include(router.urls)),
    path('products', ProductList.as_view(), name='product_list'),
    path('create/products', CreateProductProfile.as_view(), name="create_product"),
    path('sellers', SellerList.as_view(), name='seller_list'),
    path('<int:pk>/approve/seller', approve_seller, name='approve_seller'),
    path('create/profile', CreateSellerProfile.as_view(), name="create_seller"),
    path('buyers', BuyerList.as_view(), name='buyer_list'),
    path('sellerposts', SellerPostList.as_view(), name='sellerpost_list'),
    path('buyerposts', BuyerPostList.as_view(), name='buyerpost_list'),
    path('serviceproviders', ServiceProviderList.as_view(), name='serviceprovider_list'),
    path('serviceregistration', ServiceRegistrationList.as_view(), name='serviceregistration_list'),
    path('<int:pk>/view/', MapServiceDetailView.as_view(), name="map_service_detail"),  
    path('serviceproviderregistration', CreateServiceProviderProfile.as_view(), name='serviceprovider_registration'),
    path('create/service', CreateServiceView.as_view(), name='service_registration'),
    path('contactdetails', ContactDetailsList.as_view(), name='contactdetails_list'),
    path('logistics', LogiticsList.as_view(), name='logistics_list'),
    # path('storages', StorageList.as_view(), name='storage_list'),
    # path('packagings', PackagingList.as_view(), name='packaging_list'),
    # path('medicals', MedicalList.as_view(), name='medical_list'),
    path('soilsciences', SoilScienceList.as_view(), name='soilscience_list'),
    path('<int:pk>/approve/', approve_serviceprovider, name='aprrove'),    
    path('ajax/load-districts/', views.load_districts, name='ajax_load_districts'),  # <-- this one here
    path('<int:pk>/edit/', UpdateServiceProviderProfile.as_view(), name="edit_service_provider_profile"),
    path('<int:pk>/viewprovider/', ServiceProviderProfileDetailView.as_view(), name="view_serviceprovider_profile"),
    path('<int:pk>/editservice/', EditServiceView.as_view(), name="edit_service_profile"),
    path('<int:pk>/viewservice/', ServiceDetailView.as_view(), name="view_service"),
    
    
]


