from rest_framework import serializers
from .models import (Product,
                     Seller,
                     Buyer,
                     SellerPost,
                     BuyerPost,
                     ServiceProvider,
                     Service,
                     ContactDetails,
                     Logistics,
                     SoilScience,Category)
from django.contrib.auth.models import User
from farm.serializers import EnterpriseSerializer
from farm.models import Enterprise
from common.serializers import UserSerializer


class ProductSerializer(serializers.ModelSerializer):
    enterprise = serializers.PrimaryKeyRelatedField(many=False, queryset=Enterprise.objects.all())
    enterprise = serializers.SlugRelatedField(many=False,read_only=True, slug_field='name')

    class Meta:
        model = Product
        fields = ('id', 'name', 'enterprise', 'local_name', 'image', 'description', 'price', 'available',
         'date_created', 'date_updated')

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields =('id','cat_name')



class SellerSerializer(serializers.ModelSerializer):
   
    full_name = serializers.SerializerMethodField(method_name='get_user_full_name',source='user')
    region = serializers.SlugRelatedField(many=False,read_only=True, slug_field='name')
    district = serializers.SlugRelatedField(many=False,read_only=True, slug_field='name')
    county = serializers.SlugRelatedField(many=False,read_only=True, slug_field='name')
    sub_county = serializers.SlugRelatedField(many=False,read_only=True, slug_field='name')
    parish = serializers.SlugRelatedField(many=False,read_only=True, slug_field='name')
    village = serializers.SlugRelatedField(many=False,read_only=True, slug_field='name')
    approver = serializers.SlugRelatedField(many=False,read_only=True, slug_field='first_name')


   # enterprise = EnterpriseSerializer()
    class Meta:
        model = Seller
        fields = ('user','full_name', 'business_number', 'business_location', 'seller_type', 'date_of_birth', 'gender',
          'major_products', 'status', 'approver','approved_date','region','district','county','sub_county'
          ,'parish','village')

    def get_user_full_name(self, obj):
        return '{} {}'.format(obj.user.first_name, obj.user.last_name)




class SellerApprovalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Seller
        fields =('status','approver','approved_date')


class BuyerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Buyer
        fields = ('user', 'created', 'modified')

class SellerPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = SellerPost
        fields = ('name', 'product', 'quantity', 'price_offer', 'delivery_option','payment_options', 'payment_mode')


class BuyerPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = BuyerPost
        fields = ('name', 'current_location', 'product', 'total_cost', 'delivery_options', 'payment_options',
         'payment_mode', 'any_other_comment')

class ServiceProviderSerializer(serializers.ModelSerializer):
    #sector = serializers.PrimaryKeyRelatedField(many=True, queryset=Sector.objects.all())
    #sector = serializers.SlugRelatedField(many=True,read_only=True, slug_field='name')
   # user = UserSerializer()
    category = serializers.SlugRelatedField(many=True,read_only=True, slug_field='cat_name')
    user = serializers.SerializerMethodField(method_name='get_user_full_name')
    
    class Meta:
        model = ServiceProvider
        fields = ('user_id','user',  'nin','service_provider_location','category', 'list_of_services_if_more_than_one', 'is_the_service_available', 'service_location', 'is_the_service_at_a_fee','status', 'approver', 'approved_date'
       )
    '''
    returns yes or no for boolean fields
    '''
    def conversion_bool(self, instance):
        if instance.is_the_service_available == True:
            return "Yes"
        else:
            return "No"


    def get_user_full_name(self, obj):
        return '{} {}'.format(obj.user.first_name, obj.user.last_name)


class PostServiceProviderSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceProvider
        exclude=['user']

class ServiceProviderApprovalSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceProvider
        fields =('status','approver','approved_date')


class ServiceRegistrationSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField(method_name='get_user_full_name')
    full_name = serializers.SerializerMethodField(method_name='get_user_full_name',source='user')
    #category = serializers.SlugRelatedField(many=True,read_only=True, slug_field='name')
    category = serializers.SlugRelatedField(many=False,read_only=True, slug_field='cat_name')
    location = serializers.CharField(source='compute_location')


    class Meta:
        model = Service
        fields = ('id','user', 'service_name', 'size','category', 'availability_date', 'terms_and_conditions', 'availability_time', 'picture','description',
        'available_services','rent','name_of_storage_center','location_of_storage_center','certification_status',
        'vehicle_type','vehicle_capacity','location','others','full_name')

    def get_user_full_name(self, obj):
        return '{} {}'.format(obj.user.first_name, obj.user.last_name)


class PostServiceRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        exclude=['user']

class ContactDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactDetails
        fields = ('name', 'phone_number')


class LogisticsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Logistics
        fields = ('name', 'source', 'destination', 'quantity', 'time', 'product', 'payment_mode',
        'contact_details')

class SoilScienceSerializer(serializers.ModelSerializer):
    class Meta:
        model = SoilScience
        fields = ('name', 'location', 'status', 'operation_mode', 'time')
