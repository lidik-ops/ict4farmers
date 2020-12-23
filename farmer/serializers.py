from rest_framework import serializers
from .models import Group, FarmerProfile
from django.contrib.auth.models import User
from farm .models import Sector
from common .serializers import UserSerializer


class GroupSerializer(serializers.ModelSerializer):

    class Meta:
        model = Group
        fields = ('id','name', 'description', 'logo', 'address', 'contact_person', 'contact_person_email',
        'contact_person_phone')


class FarmerProfileSerializer(serializers.ModelSerializer):

    user_id = serializers.SerializerMethodField(method_name='get_id')
    user = serializers.SerializerMethodField(method_name='get_user_full_name')
    sector = serializers.SlugRelatedField(many=True,read_only=True, slug_field='name')
    group = serializers.SlugRelatedField(many=False,read_only=True, slug_field='name')
    credit_access = serializers.SerializerMethodField(method_name='conversion_bool',source='Credit access')
    full_name = serializers.SerializerMethodField(method_name='get_user_full_name',source='user')
    region = serializers.SerializerMethodField(method_name='get_region',source='user.profile.region')
    district = serializers.SerializerMethodField(method_name='get_district',source='user.profile.district')
    county = serializers.SerializerMethodField(method_name='get_county',source='user.profile.county')
    sub_county = serializers.SerializerMethodField(method_name='get_sub_county',source='user.profile.sub_county')
    parish = serializers.SerializerMethodField(method_name='get_parish',source='user.profile.parish')
    village = serializers.SerializerMethodField(method_name='get_village',source='user.profile.village')
    phone_1 = serializers.SerializerMethodField(method_name='get_phone1',source='user.profile.phone_number')
    phone_2 = serializers.SerializerMethodField(method_name='get_phone2',source='user.profile.phone_2')

    class Meta:
        model = FarmerProfile
        fields = ('user_id','user','full_name', 'date_of_birth', 'nin', 'sector', 'occupation', 'level_of_education', 'marital_status','region',
        'district','county','sub_county','parish','village','phone_1','phone_2','size_of_land', 'group', 'type_of_land', 'production_scale', 'number_of_dependants',
        'credit_access','source_of_credit', 'experience', 'status', 'general_remarks', 'approver', 'approved_date')
    '''
    returns yes or no for boolean fields
    '''
    def conversion_bool(self, instance):
        if instance.credit_access == True:
            return "Yes"
        else:
            return "No"

    def get_id(self, obj):
        return '{}'.format(obj.user.id)


    def get_user_full_name(self, obj):
        return '{} {}'.format(obj.user.first_name, obj.user.last_name)

    def get_region(self, obj):
        try:
            return '{}'.format(obj.user.profile.region)
        except:
            return None
    
    def get_district(self, obj):
        try:
            return '{}'.format(obj.user.profile.district)
        except:
            return None
    
    def get_county(self, obj):
        try:
            return '{}'.format(obj.user.profile.county)
        except:
            None

    def get_sub_county(self, obj):
        try:
            return '{}'.format(obj.user.profile.sub_county)
        except:
            return None
    
    def get_parish(self, obj):
        try:
            return '{}'.format(obj.user.profile.parish)
        except:
            return None
    
    def get_village(self, obj):
        try:
            return '{}'.format(obj.user.profile.village)
        except:
            return None

    def get_phone1(self, obj):
        try:
            return '{}'.format(obj.user.profile.phone_number)
        except:
            return None
    
    def get_phone2(self, obj):
        try:
            return '{}'.format(obj.user.profile.phone_2)
        except:
            return None
    

class PostFarmerProfileSerializer(serializers.ModelSerializer):

  
    class Meta:
        model = FarmerProfile
        exclude=['user','created','modified']
        #exclude=['created','modified']



class FarmerApprovalSerializer(serializers.ModelSerializer):
    class Meta:
        model = FarmerProfile
        fields =('status','approver','approved_date')
