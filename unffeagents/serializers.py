from rest_framework import serializers
from .models import (AgentProfile, Market, MarketPrice, Notice,Call,CallRsponse)
from django.contrib.auth.models import User


class AgentProfileSerializer(serializers.ModelSerializer):
    user_names = serializers.SerializerMethodField(method_name='get_user_full_name', read_only=True)
    region = serializers.SlugRelatedField(many=False,read_only=True, slug_field='name')
    user = serializers.SlugRelatedField(many=False,read_only=True, slug_field='username')
    district = serializers.SlugRelatedField(many=False,read_only=True, slug_field='name')
    class Meta:
        model = AgentProfile
        fields = ['id','user', 'contact', 'region', 'district', 'specific_role','user_names']

    def get_user_full_name(self, obj):
        return '{} {}'.format(obj.user.first_name, obj.user.last_name)



class MarketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Market
        fields = ['market_name', 'latitude', 'longitude', 'market_description']


class MarketPriceSerializer(serializers.ModelSerializer):
    class Meta:
        model = MarketPrice
        fields = ['market', 'user', 'product', 'unit_of_measure', 'start_price', 'end_price']

class NoticeSerializer(serializers.ModelSerializer):
    sector = serializers.SlugRelatedField(many=True,read_only=True, slug_field='name')
    district = serializers.SlugRelatedField(many=True,read_only=True, slug_field='name')
    region = serializers.SlugRelatedField(many=True,read_only=True, slug_field='name')
    county = serializers.SlugRelatedField(many=True,read_only=True, slug_field='name')
    sub_county = serializers.SlugRelatedField(many=True,read_only=True, slug_field='name')
    parish = serializers.SlugRelatedField(many=True,read_only=True, slug_field='name')
    target_audience = serializers.SlugRelatedField(many=True,read_only=True, slug_field='name')
    village = serializers.SlugRelatedField(many=True,read_only=True, slug_field='name')
    display_up_to = serializers.DateTimeField()
  
    class Meta:
        model = Notice
        fields ='__all__'


class CallSerializer(serializers.ModelSerializer):
    call_date = serializers.DateTimeField()
    responses = serializers.StringRelatedField(many=False)

    class Meta:
        model = Call
        fields = '__all__'


class ResponseSerializer(serializers.ModelSerializer):
    called_from = serializers.SlugRelatedField(many=False,read_only=True, slug_field='name')
    type_of_question = serializers.CharField(source='get_type_of_question_display')
    agent = serializers.SerializerMethodField(method_name='get_agent_name',source='agent')
    class Meta:
        model = CallRsponse
        fields = '__all__'
    

    def get_agent_name(self, obj):
        try:
            return '{} {}'.format(obj.agent.first_name, obj.agent.last_name)
        except:
            return None