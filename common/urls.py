from django.contrib.auth import views as auth_views
from common.views import (
    HomePage, account_activation_sent, activate, SignUpView, ProfileView,
    ForgotPasswordView, load_districts, load_counties,load_sub_counties,
    load_parishes,load_villages, activate,ChangePasswordView,account_activated
)

from django.urls import path,include
from rest_framework import routers
from . import views



router = routers.DefaultRouter()

router.register(r'register', views.UserViewSet,'users')
router.register(r'groups', views.GroupViewSet,'groups')
router.register(r'counties',views.CountyViewSet,'counties')
router.register(r'sub_counties',views.SubCountyViewSet,'sub_counties')
router.register(r'districts', views.DistrictViewSet,'districts')
router.register(r'parishes',views.ParishViewSet,'parishes')
router.register(r'villages',views.VillageViewSet, 'villages')
router.register(r'post_users', views.PostUserDataViewSet, 'post_users')
router.register(r'profiles', views.PostProfileViewSet, 'profiles')
router.register(r'regions',views.RegionViewSet, 'regions')


app_name ='common'

urlpatterns = [
    path('api/', include(router.urls)),
    path('', HomePage.as_view(), name='home'),
    path('account/change_password', ChangePasswordView.as_view(), name='change_password'),
    path('account_activation_sent/', account_activation_sent, name='account_activation_sent'),
    path('signup/', SignUpView.as_view(), name='signup'),
    path('activate/<uidb64>/<token>/', activate, name='activate'),
    path('account/activated', account_activated, name='activated'),
    path('forgot-password/', ForgotPasswordView.as_view(), name='forgot_password'),
    path('<int:pk>/view/profile', ProfileView.as_view(), name="view_profile"),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    # load districts url
    path('ajax/load-districts/', load_districts, name='ajax_load_districts'),
    path('ajax/load-counties/', load_counties, name='ajax_load_counties'),
    path('ajax/load-sub_counties/', load_sub_counties, name='ajax_load_sub_counties'),
    path('ajax/load-parishes/', load_parishes, name='ajax_load_parishes'),
    path('ajax/load-villages/', load_villages, name='ajax_load_villages'),

   
] 
