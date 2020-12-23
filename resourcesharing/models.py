from django.db import models
from django.contrib.auth.models import User
from common.choices import(RESOURCE_CATEGORY, PAYMENT_MODE,PAYMENT_OPTIONS)
from farmer.models import FarmerProfile
from phonenumber_field.modelfields import PhoneNumberField
from django.utils.translation import ugettext as _
from geopy.geocoders import Nominatim
from django.contrib.auth.models import User
# Create your models here.
class Resource(models.Model):
    RESOURCE_STATUS = (
         (None, "---please select---"),
        ('available', 'Available'),
        ('not available', 'Not Available')
    )
    resource_name = models.CharField(max_length=200, blank = False)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    Phone_number1 = PhoneNumberField(_('Phone number 1'), blank=False, null=True)
    Phone_number2 = PhoneNumberField(_('Phone number 2'), blank=False, null=True)
    resource_category = models.CharField(choices=RESOURCE_CATEGORY, max_length=25, null=False, blank=False)
    lat = models.FloatField(_('Latitude'), blank=True, null=True, help_text="Latitude of your location")
    lon = models.FloatField(_('Longitude'), blank=True, null=True, help_text="Longitude of your location")
    terms_and_conditions = models.TextField(max_length=400, blank = False)
    resource_status = models.CharField(max_length=20, choices=RESOURCE_STATUS)
    available_from = models.DateField(auto_now=True)
    available_to = models.DateField(auto_now=True)
    image = models.ImageField(null=True, blank=False)
    price = models.DecimalField(_('Price(shs)'),decimal_places=2, max_digits=20, blank=False)

    def __str__(self):
        return self.resource_name

    class Meta:
        permissions = (
            ("can_approve_resourcebooking", "Can approve resourcebooking"),
        )

    class Meta:
        permissions = (
            ("can_cancel_resourcebooking", "Can cancel resourcebooking"),
        )

    @property
    def compute_location(self):
        geolocator = Nominatim(user_agent="ICT4Farmers", timeout=10)
        lat = str(self.lat)
        lon = str(self.lon)
       
        try:

            location = geolocator.reverse(lat + "," + lon)
            return '{}'.format(location)
        except:
            location = str(self.lat) + "," + str(self.lon)
            return 'slow network, loading location ...'

class ResourceSharing(models.Model):
    resource = models.ForeignKey(Resource, on_delete = models.CASCADE)
    date_taken = models.DateTimeField(blank = False, null=False)
    expected_return_date = models.DateTimeField(blank=False, null=False)
    # taken_by = models.ForeignKey(User)
    taken_by = models.CharField(max_length=100,null=False)
    phone_1 = PhoneNumberField(verbose_name='contact phone of person who took the resource')
    phone_2 = PhoneNumberField(verbose_name='contact phone of person who took the resource')

    def __str__(self):
        return self.resource


class ResourceBooking(models.Model):
    resource = models.ForeignKey(Resource, on_delete = models.CASCADE)
    booker = models.CharField(max_length=25,null=True, blank=True)
    date_needed = models.DateTimeField(blank = True)
    payment_mode = models.CharField(choices=PAYMENT_MODE, null=True, blank=True, max_length=25)
    payment_method = models.CharField(choices=PAYMENT_OPTIONS, max_length=25,null=True, blank=True)

    def __str__(self):
        return self.resource
