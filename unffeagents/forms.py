from django import forms
from .models import AgentProfile, Notice,CallRsponse
from phonenumber_field.formfields import PhoneNumberField
from phonenumber_field.widgets import PhoneNumberPrefixWidget
from common .models import (Region,District)
from farm .models import Sector
from django.shortcuts import render
from django.utils.safestring import mark_safe
from django.contrib.auth.models import User

class CustomUserChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
         return obj.get_full_name()

class AgentProfileForm(forms.ModelForm):
    contact = PhoneNumberField(widget=PhoneNumberPrefixWidget(attrs={'class': 'form-control','style': 'width:50%; display:inline-block;'}), required=True, initial='+256')
    district = forms.ModelChoiceField(widget=forms.Select(attrs={'class': 'form-control'}), queryset=District.objects.none())
    user = CustomUserChoiceField(queryset=User.objects.all())
    class Meta:
        model = AgentProfile
        exclude = []

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(AgentProfileForm, self).__init__(*args, **kwargs)
        self.fields['user'].empty_label = '--please select--'
        self.fields['district'].label = 'Allocate District'
        self.fields['district'].empty_label = '--please select--'
        self.fields['region'].label = 'Allocate Region'
        self.fields['region'].empty_label = '--please select--'
        self.fields['specific_role'].empty_label = '--please select--'

        if 'region' in self.data:
            try:
                region_id = int(self.data.get('region'))
                self.fields['district'].queryset = District.objects.filter(region_id=region_id).order_by('name')
            except (ValueError, TypeError):
                pass  # invalid input from the client; ignore and fallback to empty district queryset
        elif self.instance.pk:
            self.fields['district'].queryset = self.instance.region.district_set.order_by('name')



class NoticeForm(forms.ModelForm):
    display_up_to = forms.DateField(widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}))
  
        
    class Meta:
        model = Notice
        exclude = ['posted_by']

    def __init__(self, *args, **kwargs):
        super(NoticeForm, self).__init__(*args, **kwargs)
        self.fields['description'].widget.attrs.update({'rows': '3'})
        self.fields['sector'].empty_label = None
        self.fields['region'].empty_label = None
        self.fields['sector'].widget = forms.CheckboxSelectMultiple()
        self.fields['region'].widget = forms.CheckboxSelectMultiple()
       
class EnquiryForm(forms.ModelForm):
    #caller = PhoneNumberField(widget=PhoneNumberPrefixWidget(attrs={'class': 'form-control','style': 'width:50%; display:inline-block;'}), required=True, initial='+256')

     
    class Meta:
        model = CallRsponse
        exclude = ['agent','call','caller']

    def __init__(self, *args, **kwargs):
        super(EnquiryForm, self).__init__(*args, **kwargs)
        self.fields['question'].widget.attrs.update({'rows': '3'})
        self.fields['called_from'].empty_label = None
        self.fields['solution'].widget.attrs.update({'rows': '3'})
