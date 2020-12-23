from .models  import Resource, ResourceBooking
from django import forms
from phonenumber_field.formfields import PhoneNumberField
from phonenumber_field.widgets import PhoneNumberPrefixWidget




class ResourceForm(forms.ModelForm):
    Phone_number1 = PhoneNumberField(widget=PhoneNumberPrefixWidget(attrs={'class': 'form-control','style': 'width:50%; display:inline-block;'}), required=True, initial='+256')
    Phone_number2 = PhoneNumberField(widget=PhoneNumberPrefixWidget(attrs={'class': 'form-control','style': 'width:50%; display:inline-block;'}), required=True, initial='+256')
    available_from = forms.DateField(widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}))
    available_to = forms.DateField(widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}))
    class Meta:
        model = Resource
        exclude = ['owner']

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(ResourceForm, self).__init__(*args, **kwargs)
        self.fields['terms_and_conditions'].widget.attrs.update({'rows': '3'})
      
class ResourceBookingForm(forms.ModelForm):
    date_needed = forms.DateField(widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}))
   
    class Meta:
        model = ResourceBooking
        exclude = ['booker']

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(ResourceBookingForm, self).__init__(*args, **kwargs)
       
    