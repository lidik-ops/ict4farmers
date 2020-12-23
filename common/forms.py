from django import forms
from django.contrib.auth.models import User
from .models import Profile
from django.contrib.auth import authenticate
from django.contrib.auth.forms import UserCreationForm
from phonenumber_field.formfields import PhoneNumberField
from phonenumber_field.widgets import PhoneNumberPrefixWidget
from django.contrib.auth.forms import PasswordResetForm
from .choices import *
from .models import Region,District,County,SubCounty,Parish,Village


# login form
class LoginForm(forms.ModelForm):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'password']

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request", None)
        super(LoginForm, self).__init__(*args, **kwargs)

    def clean_password(self):
        password = self.cleaned_data.get('password')
        if password:
            if len(password) < 4:
                raise forms.ValidationError(
                    'Password must be at least 4 characters long!')
        return password

    def clean(self):
        username = self.cleaned_data.get("username")
        password = self.cleaned_data.get("password")


        if username and password:
            self.user = authenticate(username=username, password=password)
            if self.user:
                if not self.user.is_active:
                    pass
                    # raise forms.ValidationError("User is Inactive")
            else:
                pass
                # raise forms.ValidationError("Invalid email and password")
        return self.cleaned_data

# sign up form

class SignUpForm(UserCreationForm):

    username = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}),required=True)
    email = forms.EmailField(widget=forms.TextInput(attrs={'class':'form-control'}),required=False)
    first_name = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}),required=True)
    last_name = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}),required=True)
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control'}),required=True, label="Enter Password")
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control'}),required=True, label="Confirm Password")
    home_address = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'cols': 30}),
                                        required=False)
    phone_number = PhoneNumberField(widget=PhoneNumberPrefixWidget(attrs={'class': 'form-control','style': 'width:50%; display:inline-block;'}), required=True, initial='+256')
    phone_2 = PhoneNumberField(widget=PhoneNumberPrefixWidget(attrs={'class': 'form-control','style': 'width:50%; display:inline-block;'}), required=False, initial='+256')
    gender = forms.CharField(widget=forms.Select(choices=GENDER_CHOICES, attrs={'class':'form-control'}),required=True)
    profile_pic = forms.ImageField(required=False)
    region = forms.ModelChoiceField(widget=forms.Select(attrs={'class': 'form-control'}), queryset=Region.objects.all())
    district = forms.ModelChoiceField(widget=forms.Select(attrs={'class': 'form-control'}), queryset=District.objects.none())
    county = forms.ModelChoiceField(widget=forms.Select(attrs={'class': 'form-control'}), queryset=County.objects.none())
    sub_county = forms.ModelChoiceField(widget=forms.Select(attrs={'class': 'form-control'}), queryset=SubCounty.objects.none())
    parish = forms.ModelChoiceField(widget=forms.Select(attrs={'class': 'form-control'}), queryset=Parish.objects.none())
    village = forms.ModelChoiceField(widget=forms.Select(attrs={'class': 'form-control'}), queryset=Village.objects.none())

    class Meta:
        model = User
        fields = ['username','first_name', 'last_name', 'email','password1', 'password2','phone_number','phone_2','home_address','gender', 'profile_pic','region','district','county','sub_county','parish','village' ]
    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)
        self.fields['district'].empty_label = '--please select--'
        self.fields['region'].empty_label = '--please select--'
        self.fields['county'].empty_label = '--please select--'
        self.fields['sub_county'].empty_label = '--please select--'
        self.fields['parish'].empty_label = '--please select--'
        self.fields['village'].empty_label = '--please select--'

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

   




class ProfileForm(forms.ModelForm):
    home_address = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'cols': 30}),
                                        required=False)
    phone_number = PhoneNumberField(widget=PhoneNumberPrefixWidget(attrs={'class': 'form-control','style': 'width:50%; display:inline-block;'}), required=True)

    class Meta:
        model = Profile
        fields = ('phone_number', 'home_address', 'gender', 'region','district','county','sub_county','parish','village')



class PasswordResetEmailForm(PasswordResetForm):

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not User.objects.filter(email__iexact=email,
                                   is_active=True).exists():
            raise forms.ValidationError("User doesn't exist with this Email")
        return email

