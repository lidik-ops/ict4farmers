from django import forms
from .models import FarmerProfile, Group
from phonenumber_field.formfields import PhoneNumberField
from phonenumber_field.widgets import PhoneNumberPrefixWidget
from common .models import(District, County, SubCounty, Parish, Village)
from common .choices import PAST_YEARS


class FarmerProfileForm(forms.ModelForm):
    date_of_birth = forms.DateField(widget=forms.SelectDateWidget(years=PAST_YEARS,attrs={'class': 'form-control','style':'display:inline-block; width:33%; '}))
   


    class Meta:
        model = FarmerProfile
        exclude = ['user','status','approver','approved_date']

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(FarmerProfileForm, self).__init__(*args, **kwargs)
        self.fields['general_remarks'].widget.attrs.update({'rows': '2'})
        self.fields['group'].empty_label = None
       
      

class FarmerGroupForm(forms.ModelForm):

    contact_person_phone = PhoneNumberField(widget=PhoneNumberPrefixWidget(attrs={'class': 'form-control','style': 'width:50%; display:inline-block;'}), required=True, initial='+256')


    class Meta:
        model = Group
        exclude = []

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(FarmerGroupForm, self).__init__(*args, **kwargs)
        self.fields['description'].widget.attrs.update({'rows': '2'})
        self.fields['address'].widget.attrs.update({'rows': '2'})
            