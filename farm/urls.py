from django.urls import include, path
from rest_framework import routers
from . import views
from .views import (SectorList, SectorDetail, CreateSector,EnterpriseList, FarmListView, FarmViewSet, 
CreateFarmView, EditFarmView,FarmproductionRecordsList,FarmproductionRecordsList,CreateFarmProductionRecordView,FarmMapViewSet,CreateEnterpriseView,EditEnterpriseView,CreateQueryView,
FarmProfileDetailView,QueryList,CreateFarmRecordView, FarmRecordsList, EditFarmRecordView,
CreateFarmFinancialRecordView,EditFarmproductionRecordView, EditFarmFinancialRecordView, FarmFinancilRecordsList,EditQueryView, EnterpriseSelectionView,
EnterpriseSelectionRedirect,EnterpriseSelectionDetailView)


router = routers.DefaultRouter()

router.register(r'farms', views.FarmViewSet,'farm-api')
router.register(r'maps', views.FarmMapViewSet,'maps-api')
router.register(r'sector', views.SectorViewSet,'apisector')
router.register(r'enterpriseselection', views.EnterpriseSelectionViewSet,'api-enterpriseselection' )
router.register(r'enterprise', views.EnterpriseViewSet, basename='Enterprise')
router.register(r'farmrecords', views.FarmRecordViewSet, basename='FarmRecord')
router.register(r'financialrecords',views.FarmFinancialRecordViewSet,'FinancialRecord')
router.register(r'productionrecords',views.FarmProductionRecordViewSet,'ProductionRecord')
router.register(r'query', views.QueryViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.

app_name = 'farm'
urlpatterns = [
    path('api/', include(router.urls)),
    path('list', FarmListView.as_view(), name='farm_list'),
    path('create', CreateFarmView.as_view(), name="create_farm"),
    path('sectors', SectorList.as_view(), name='sector_list'),
    path('<int:pk>/edit/farm', EditFarmView.as_view(), name="edit_farm"),
    path('<int:pk>/edit/sector', SectorDetail.as_view(), name="edit_sector"),
    path('create/sector', CreateSector.as_view(), name="create_sector"),
    path('create/query', CreateQueryView.as_view(), name="create_query"),
    path('<int:pk>/edit/query', EditQueryView.as_view(), name="edit_query"),
    path('queries', QueryList.as_view(), name='query_list'),
    path('enterprises', EnterpriseList.as_view(), name='enterprise_list'),
    path('create/enterprise/<int:farm_pk>', CreateEnterpriseView.as_view(), name="create_enterprise"),
    path('<int:pk>/edit/enterprise', EditEnterpriseView.as_view(), name="edit_enterprise"),
    path('<int:pk>/view/', FarmProfileDetailView.as_view(), name="view_farm_profile"),  
    path('create/record/<int:enterprise_pk>', CreateFarmRecordView.as_view(), name="create_farm_record"), 
    path('farmrecords', FarmRecordsList.as_view(), name='farmrecords') ,
    path('<int:pk>/edit/farmrecord', EditFarmRecordView.as_view(), name="edit_farmrecord"),
    path('create/financilrecord/<int:enterprise_pk>', CreateFarmFinancialRecordView.as_view(), name="create_financial_record"), 
    path('financialrecords', FarmFinancilRecordsList.as_view(), name='financialrecords') ,
    path('<int:pk>/edit/financialrecord', EditFarmFinancialRecordView.as_view(), name="edit_financail_record"),
    path('create/productionrecord/<int:enterprise_pk>', CreateFarmProductionRecordView.as_view(), name="create_production_record"), 
    path('productionrecords', FarmproductionRecordsList.as_view(), name='productionrecords') ,
    path('<int:pk>/edit/productionrecord', EditFarmproductionRecordView.as_view(), name="edit_production_record"),
    path('create/enterpriseselection', EnterpriseSelectionView.as_view(), name='enterprise_selection'),
    path('selectenterprises', EnterpriseSelectionRedirect.as_view(), name='select_enterpise'),
    path('<int:pk>/view/selectenterprise', EnterpriseSelectionDetailView.as_view(), name="view_enterprise_selection"),
    #path('viewselectenterprises', EnterpriseSelectionDetailView.as_view(), name='enterprise_selection_detail'),
]
