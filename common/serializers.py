from rest_framework import serializers
from django.contrib.auth.models import User,Group
from .models import Region, District, County, SubCounty, Parish, Village, Profile
from django.contrib.auth.models import Group as UserGroup
from rest_framework.authtoken.models import Token
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string


class GroupSerializer(serializers.ModelSerializer):
    permissions = serializers.SlugRelatedField(many=True,read_only=True, slug_field='name')
    name = serializers.CharField()
    
    class Meta:
        model = Group
        fields = ['id','name','permissions']


class UserSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    first_name = serializers.CharField(max_length=100)
    last_name = serializers.CharField(max_length=100)
    user_permissions = serializers.SlugRelatedField(many=True,read_only=True, slug_field='name')
    groups = GroupSerializer(many=True)
    email = serializers.EmailField()
    username = serializers.CharField(max_length=100)
    full_name = serializers.SerializerMethodField(method_name='get_user_full_name',source='username')
    phone_number = serializers.CharField(source='profile.phone_number')
    gender = serializers.CharField(source='profile.get_gender_display')
    home_address = serializers.CharField(source='profile.home_address')
    profile_pic = serializers.FileField(source='profile.profile_pic',required=False,)
    region = serializers.SlugRelatedField(many=False,read_only=True, slug_field='name')
    district = serializers.SlugRelatedField(many=False,read_only=True, slug_field='name')
    county = serializers.SlugRelatedField(many=False,read_only=True, slug_field='name')
    sub_county = serializers.SlugRelatedField(many=False,read_only=True, slug_field='name')
    parish = serializers.SlugRelatedField(many=False,read_only=True, slug_field='name')
    village = serializers.SlugRelatedField(many=False,read_only=True, slug_field='name')

    def get_user_full_name(self, obj):
        return '{} {}'.format(obj.first_name, obj.last_name)

    class Meta:
        model = User
        fields = '__all__'


class ProfileSerializer(serializers.ModelSerializer):
    #profile_pic = serializers.FileField(required=False, source='profile.profile_pic')
  
    class Meta:
        model = Profile
        fields = ['phone_number','phone_2','home_address','gender','region','district','parish','county','sub_county','village']
        

class UserPostSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer()
    class Meta:
        model = User
        fields = ('username','first_name','last_name','email','password','profile')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):

        # create user 
        user = User.objects.create(
            username = validated_data['username'],
            email = validated_data['email'],
            first_name = validated_data['first_name'],
            last_name = validated_data['last_name'],
            password = validated_data['password']
        )

        profile_data = validated_data.pop('profile')
       
        # create profile
        profile = Profile.objects.create(
            user = user,
            phone_number = profile_data['phone_number'],
            phone_2 = profile_data['phone_2'],
            home_address = profile_data['home_address'],
            gender =  profile_data['gender'],
            #profile_pic = profile_data['profile_pic'],
            region = profile_data['region'],
            district = profile_data['district'],
            county = profile_data['county'],
            sub_county = profile_data['sub_county'],
            parish = profile_data['parish'],
            village = profile_data['village']
        )
        Token.objects.get_or_create(user=user)
       
        return user


class RegionSerializer(serializers.ModelSerializer):
  
    class Meta:
        model = Region
        fields ='__all__'   

class DistrictSerializer(serializers.ModelSerializer):
  
    class Meta:
        model = District
        fields ='__all__'


class CountySerializer(serializers.ModelSerializer):
  
    class Meta:
        model = County
        fields ='__all__'

class SubCountySerializer(serializers.ModelSerializer):
  
    class Meta:
        model = SubCounty
        fields ='__all__'

class ParishSerializer(serializers.ModelSerializer):
  
    class Meta:
        model = Parish
        fields ='__all__'

class VillageSerializer(serializers.ModelSerializer):
  
    class Meta:
        model = Village
        fields ='__all__'

class UserApiPost(serializers.ModelSerializer):
    class Meta:
        model = User
        fields =['id','first_name','last_name','username']