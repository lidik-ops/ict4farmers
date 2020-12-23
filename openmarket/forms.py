from django import forms
from .models import Seller,Product,ServiceProvider, Service, Category
from common.models import Region, District, County, SubCounty, Parish, Village
from common.choices import SERVICE_CATEGORY
from phonenumber_field.formfields import PhoneNumberField
from phonenumber_field.widgets import PhoneNumberPrefixWidget


class ServiceProviderProfileForm(forms.ModelForm):
   
    
    class Meta:
        model = ServiceProvider
        exclude = ['user','status','status','approver','approved_date']

 
class SellerProfileForm(forms.ModelForm):
    date_of_birth = forms.DateField(widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}))
    business_number = PhoneNumberField(widget=PhoneNumberPrefixWidget(attrs={'class': 'form-control','style': 'width:50%; display:inline-block;'}), required=True, initial='+256')
    region = forms.ModelChoiceField(widget=forms.Select(attrs={'class': 'form-control'}), queryset=Region.objects.all())
    district = forms.ModelChoiceField(widget=forms.Select(attrs={'class': 'form-control'}), queryset=District.objects.none())
    county = forms.ModelChoiceField(widget=forms.Select(attrs={'class': 'form-control'}), queryset=County.objects.none())
    sub_county = forms.ModelChoiceField(widget=forms.Select(attrs={'class': 'form-control'}), queryset=SubCounty.objects.none())
    parish = forms.ModelChoiceField(widget=forms.Select(attrs={'class': 'form-control'}), queryset=Parish.objects.none())
    village = forms.ModelChoiceField(widget=forms.Select(attrs={'class': 'form-control'}), queryset=Village.objects.none())

    
    
    class Meta:
        model = Seller
        exclude = ['user','status', 'approver','approved_date']

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(SellerProfileForm, self).__init__(*args, **kwargs)
        self.fields['district'].empty_label = '--please select--'
        self.fields['region'].empty_label = '--please select--'
        self.fields['county'].empty_label = '--please select--'
        self.fields['sub_county'].empty_label = '--please select--'
        self.fields['parish'].empty_label = '--please select--'
        self.fields['village'].empty_label = '--please select--'
        self.fields['business_location'].widget.attrs.update({'rows': '2'})
        self.fields['major_products'].empty_label = '--please select--'

        if 'region' in self.data:
            try:
                region_id = int(self.data.get('region'))
                self.fields['district'].queryset = District.objects.filter(region_id=region_id).order_by('name')
            except (ValueError, TypeError):
                pass  # invalid input from the client; ignore and fallback to empty district queryset
        elif self.instance.pk:
            self.fields['district'].queryset = self.instance.region.district_set.order_by('name')

        if 'district' in self.data:
            try:
                district_id = int(self.data.get('district'))
                self.fields['county'].queryset = County.objects.filter(district_id=district_id).order_by('name')
            except (ValueError, TypeError):
                pass  # invalid input from the client; ignore and fallback to empty district queryset
        elif self.instance.pk:
            self.fields['county'].queryset = self.instance.district.county_set.order_by('name')
        
        if 'county' in self.data:
            try:
                county_id = int(self.data.get('county'))
                self.fields['sub_county'].queryset = SubCounty.objects.filter(county_id=county_id).order_by('name')
            except (ValueError, TypeError):
                pass  # invalid input from the client; ignore and fallback to empty district queryset
        elif self.instance.pk:
            self.fields['sub_county'].queryset = self.instance.county.subcounty_set.order_by('name')

        
        if 'sub_county' in self.data:
            try:
                sub_county_id = int(self.data.get('sub_county'))
                self.fields['parish'].queryset = Parish.objects.filter(sub_county_id=sub_county_id).order_by('name')
            except (ValueError, TypeError):
                pass  # invalid input from the client; ignore and fallback to empty district queryset
        elif self.instance.pk:
            self.fields['parish'].queryset = self.instance.sub_county.parish_set.order_by('name')
            print(self.instance.sub_county.parish_set)


        if 'parish' in self.data:
            try:
                parish_id = int(self.data.get('parish'))
                self.fields['village'].queryset = Village.objects.filter(parish_id=parish_id).order_by('name')
            except (ValueError, TypeError):
                pass  # invalid input from the client; ignore and fallback to empty district queryset
        elif self.instance.pk:
            self.fields['village'].queryset = self.instance.parish.village_set.order_by('name')

class ProductProfileForm(forms.ModelForm):
    
     class Meta:
        model = Product
        exclude = ['date_created', 'date_updated']

     def __init__(self, *args, **kwargs):
         self.request = kwargs.pop('request', None)
         super(ProductProfileForm, self).__init__(*args, **kwargs)
         self.fields['description'].widget.attrs.update({'rows': '2'})

class ServiceProfileForm(forms.ModelForm):
    availability_date = forms.DateField(widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}))
    #service_name = forms.CharField(label="Service Name")

    class Meta:
        model = Service
        exclude = ['date_created', 'date_updated','user']

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(ServiceProfileForm, self).__init__(*args, **kwargs)
        self.fields['category'].empty_label = '--please select--'
        servicecategories = ServiceProvider.objects.filter(user=self.request.user).values('category')
        self.fields['category'].queryset = Category.objects.filter(id__in = servicecategories)
