from .models  import (Farm, Enterprise,ProductionRecord, Sector, Query,FarmRecord,FinancialRecord,EnterpriseSelection)
from django import forms
from farmer.models import FarmerProfile
from phonenumber_field.formfields import PhoneNumberField
from phonenumber_field.widgets import PhoneNumberPrefixWidget



class FarmForm(forms.ModelForm):
    start_date = forms.DateField(widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}))

    class Meta:
        model = Farm
        exclude = ['status','available_land']

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(FarmForm, self).__init__(*args, **kwargs)
        self.fields['general_remarks'].widget.attrs.update({'rows': '2'})
      
class QueryForm(forms.ModelForm):
    date_discovered = forms.DateField(widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}))
    reporting_date = forms.DateField(widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}))

    class Meta:
        model = Query
        exclude = ['solution']

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(QueryForm, self).__init__(*args, **kwargs)
        self.fields['action_taken'].widget.attrs.update({'rows': '2'})
      

      
class EnterpriseForm(forms.ModelForm):
    start_date = forms.DateField(widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}))
    from_period = forms.DateField(widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}))
    to_period = forms.DateField(widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}))
    land_occupied = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'form-control'}))

    class Meta:
        model = Enterprise
        exclude = ['status']

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(EnterpriseForm, self).__init__(*args, **kwargs)
        self.fields['description'].widget.attrs.update({'rows': '2'})
        self.fields['farm'].empty_label = None
        self.fields['sector'].empty_label = '--please select--'
        farmersectors = FarmerProfile.objects.filter(user=self.request.user).values('sector')
        self.fields['sector'].queryset = Sector.objects.filter(id__in=farmersectors)
        self.fields['farm'].queryset = Farm.objects.filter(farmer_id=self.request.user.id)


class FarmRecordForm(forms.ModelForm):
    from_date = forms.DateField(widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}))
    to_date = forms.DateField(widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}))
    next_activity_date = forms.DateField(widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),required=False)
    contact = PhoneNumberField(widget=PhoneNumberPrefixWidget(attrs={'class': 'form-control','style': 'width:50%; display:inline-block;'}), required=True, initial='+256')
  
    class Meta:
        model = FarmRecord
        exclude = ['status']

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(FarmRecordForm, self).__init__(*args, **kwargs)
        self.fields['description'].widget.attrs.update({'rows': '2'})
       
        self.fields['enterprise'].empty_label = None
        farms = Farm.objects.filter(farmer_id=self.request.user.id)
        self.fields['enterprise'].queryset = Enterprise.objects.filter(farm__in=farms)


class FarmFnancialRecordForm(forms.ModelForm):
    next_payment_date = forms.DateField(widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}))
    # transaction_date = forms.DateField(widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}))
    class Meta:
        model = FinancialRecord
        exclude = ['reported_by','transaction_date']

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(FarmFnancialRecordForm, self).__init__(*args, **kwargs)
        self.fields['description'].widget.attrs.update({'rows': '2'})
        self.fields['enterprise'].empty_label = None
        farms = Farm.objects.filter(farmer_id=self.request.user.id)
        self.fields['enterprise'].queryset = Enterprise.objects.filter(farm__in=farms)

class FarmProductionRecordForm(forms.ModelForm):
    record_date = forms.DateField(widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}))
    record_time = forms.TimeField(widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'time'}))
   
    class Meta:
        model = ProductionRecord
        exclude = []

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(FarmProductionRecordForm, self).__init__(*args, **kwargs)
        self.fields['general_remarks'].widget.attrs.update({'rows': '2'})
        self.fields['enterprise'].empty_label = None
        farms = Farm.objects.filter(farmer_id=self.request.user.id)
        self.fields['enterprise'].queryset = Enterprise.objects.filter(farm__in=farms)

class EnterpriseSelectionForm(forms.ModelForm):

    class Meta:
        model=EnterpriseSelection
        exclude = ['user','recommendation']