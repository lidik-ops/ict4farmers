from django.db import models
from django.contrib.auth.models import User
from common.models import(Region, District, County, SubCounty, Parish, Village, TimeStampedModel)
from common.choices import(GENDER_CHOICES,
                           MARITAL_STATUSES,REGISTER_STATUS,
                           STATUS,INVENTORY_STATUS, TYPE,
                           PAYMENT_MODE,
                           PAYMENT_OPTIONS,
                           YES_OR_NO,
                           EDUCATION_LEVEL,
                           SERVICE_CATEGORY)
from django.core.validators import RegexValidator
from farm.models import Enterprise
from phonenumber_field.modelfields import PhoneNumberField
from django.utils.translation import ugettext as _
from geopy.geocoders import Nominatim
# Create your models here.phone_2 = PhoneNumberField(widget=PhoneNumberPrefixWidget(attrs={'class': 'form-control','style': 'width:50%; display:inline-block;'}), required=True, initial='+256')

class Product(models.Model):
    name = models.CharField(max_length=50, null=True)
    enterprise = models.ForeignKey(to='farm.Enterprise',related_name='products',on_delete=models.CASCADE)
    local_name = models.SlugField(max_length=200,null=True, db_index=True)
    image = models.ImageField(upload_to='products/%Y/%m/%d',blank=True)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    available = models.BooleanField(default=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Seller(models.Model):
    #personal information
    user = models.OneToOneField(User, on_delete=models.CASCADE, unique=True, related_name='seller',primary_key=True)
    date_of_birth = models.DateField(max_length=8)
    gender = models.CharField(choices=GENDER_CHOICES, max_length=15)
    seller_type = models.CharField(choices=TYPE,max_length=15, null=False)
    major_products = models.CharField(max_length=50,blank=True)

    #Location
    business_number = PhoneNumberField()
    business_location = models.TextField(_('Business Address'),null=True)
    region = models.ForeignKey(Region, on_delete=models.CASCADE)
    district = models.ForeignKey(District, on_delete=models.CASCADE)
    county = models.ForeignKey(County, on_delete=models.CASCADE)
    sub_county = models.ForeignKey(SubCounty, on_delete=models.CASCADE)
    parish = models.ForeignKey(Parish, on_delete=models.CASCADE)
    village = models.ForeignKey(Village, on_delete=models.CASCADE)

    status = models.CharField(choices=REGISTER_STATUS, default='in_active', max_length=20,null=False)
      # handle approving of a seller
    approver = models.ForeignKey(User, on_delete=models.DO_NOTHING,related_name="seller_unffe_agent",null=True,blank=True)
    approved_date = models.DateTimeField(blank=True, null=True)

    class Meta:
        ordering = ('seller_type',)
        permissions = (
            ("can_approve_sellers", "Can approve Sellers"),
        )
    def __str__(self):
        return self.seller_type

class Buyer(TimeStampedModel, models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='buyer')

    class meta:
        ordering =("created")


class SellerPost(models.Model):
    name = models.ForeignKey(Seller, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.FloatField(max_length=50, null=True)
    price_offer = models.DecimalField(max_digits=10, decimal_places=2)
    delivery_option = models.CharField(max_length=50)
    payment_options = models.CharField(choices=PAYMENT_OPTIONS, max_length=50, null=True)
    payment_mode = models.CharField(choices=PAYMENT_MODE, null=True, max_length=50)

    class Meta:
        ordering = ('-name',)


class BuyerPost(models.Model):
    name = models.ForeignKey(Buyer, on_delete=models.CASCADE)
    current_location = models.CharField(max_length=50)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.FloatField(max_length=50, null=True)
    total_cost = models.DecimalField(max_digits=10, decimal_places=2)
    delivery_options = models.CharField(max_length=50, null=False)
    payment_options = models.CharField(choices=PAYMENT_OPTIONS, max_length=50, null=True)
    payment_mode = models.CharField(choices=PAYMENT_MODE, null=True, max_length=50)
    any_other_comment =models.TextField(null=True)

    class meta:
        ordering =("name",)



class Category(TimeStampedModel, models.Model):
    cat_name = models.CharField(max_length=255)
   
    def __str__(self):
        return self.cat_name


class ServiceProvider(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, unique=True, related_name='serviceprovider',primary_key=True)
    nin = models.CharField(_('National Identity Number (NIN)'),max_length=14, null=True, blank=False)
    service_provider_location = models.CharField(null=True, max_length=50)
    list_of_services_if_more_than_one = models.CharField(blank=True, max_length=50)
    is_the_service_available = models.BooleanField(choices=YES_OR_NO, null=True)
    service_location = models.CharField(max_length=100, null=True)
    is_the_service_at_a_fee = models.BooleanField(choices=YES_OR_NO, null=True)
   # category = models.ManyToManyField(to='openmarket.Category', related_name='enterprise categories', choices=)
    category = models.ManyToManyField(Category, related_name='Categories')
    status = models.CharField(choices=STATUS, default='Pending', max_length=20,null=False)
    # handle approving of a farmer
    approver = models.ForeignKey(User, on_delete=models.DO_NOTHING,related_name="unffe_agent_service_provider",null=True,blank=True)
    approved_date = models.DateTimeField(blank=True, null=True)



    class meta:
        ordering =("nin")
        permissions = (
            ("can_approve_service_providers", "Can approve service providers"),
        )

class Service(models.Model):
    enterprise = models.CharField(max_length=50, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='service',null=True)
    category = models.ForeignKey(Category, on_delete= models.CASCADE, null=True)
    service_name = models.CharField(max_length=200, null=True)
    #service_type = models.CharField(max_length=50, null=True)
    size =  models.FloatField(max_length=50, null=True,blank=True)
    terms_and_conditions = models.BooleanField(default=True)
    availability_date = models.DateField(blank=True, null=True)
    availability_time = models.DateTimeField(auto_now_add=True, null=True)
    picture = models.ImageField(null=True, blank=True)
    description = models.TextField(blank=True)
    available_services = models.CharField(max_length=50, blank=True)
    rent = models.CharField(max_length=25, null=True, blank=True)
    name_of_storage_center = models.CharField(max_length=50, null=True,blank=True)
    location_of_storage_center = models.CharField(null=True, max_length=50, blank=True)
    certification_status = models.BooleanField(_('Is the Service Certified'),choices = YES_OR_NO, null=True, blank=True)
    vehicle_type = models.CharField(max_length=100, null = True, blank=True)
    vehicle_capacity = models.FloatField(max_length=50, null=True, help_text="capacity of your vehicle in tonnes", blank=True)
    lat = models.FloatField(_('Latitude'), blank=True, null=True, help_text="Latitude of your industry location")
    lon = models.FloatField(_('Longitude'), blank=True, null=True,help_text="Longitude of your industry location")
    others = models.CharField(_('Please state the category if its not among the above'), blank=True, null=True, max_length=100)
    driver_contact =  PhoneNumberField(null=True, blank=True)
    driver_name =  models.CharField(max_length = 100, null=True, blank = True)


    class meta:
        ordering =("service_type")
    
    @property
    def compute_location(self):
        geolocator = Nominatim(user_agent="ICT4Farmers", timeout=10)
        lat = str(self.lat)
        lon = str(self.lon)

        try:

            location = geolocator.reverse(lat + "," + lon)
            return '{}'.format(location)
        except:
            #location = str(self.lat) + "," + str(self.lon)
            return 'slow network, loading location ...'



class ContactDetails(models.Model):
    name = models.CharField(max_length=25, null=True)
    #phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
    phone_number = PhoneNumberField() # validators should be a list


    class Meta:
        ordering =("name",)

class Logistics(models.Model):
    name = models.ForeignKey(ServiceProvider, on_delete=models.CASCADE)
    source = models.CharField(max_length=50, null=True)
    destination = models.CharField(max_length=50, null=True)
    quantity = models.FloatField(max_length=50, null=True)
    time = models.DateTimeField(auto_now_add=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    payment_mode = models.CharField(choices=PAYMENT_MODE, null=True, max_length=50)
    contact_details = models.ForeignKey(ContactDetails, on_delete=models.CASCADE)


    class Meta:
        ordering =("name",)

# class Storage(models.Model):
#     storage = models.ForeignKey(Service, on_delete=models.CASCADE, null=True)

#     size = models.FloatField(null=True)
#     type = models.CharField(max_length=50, null=False)



# class Packaging(models.Model): #value addition.
#     name = models.CharField(max_length=50, null=True)
#     product = models.ForeignKey(Product, on_delete=models.CASCADE)
#     location = models.CharField(null=True, max_length=50)
#     image = models.ImageField(upload_to='products/%Y/%m/%d',blank=True)
#     status = models.CharField(choices=STATUS, default='True', max_length=20, null=False)
#     #rent = models.CharField(max_length=25, null=True)

#     class Meta:
#         ordering =("name",)

# class Medical(models.Model):
#     name = models.CharField(max_length=50, null=True)
#     enterprise = models.ForeignKey(to='farm.Enterprise',related_name='medical',on_delete=models.CASCADE)
#     location = models.CharField(null=True, max_length=50)
#     status = models.CharField(choices=STATUS, default='True', max_length=20, null=False)
#     time = models.DateTimeField(auto_now_add=True)

#     class Meta:
#         ordering =("name",)


class SoilScience(models.Model):
    name = models.CharField(max_length=50, null=True)
    location = models.CharField(null=True, max_length=50)
    operation_mode = models.CharField(max_length=50, null=True)
    time = models.DateTimeField(auto_now_add=True)
    status = models.CharField(choices=STATUS, default='True', max_length=20, null=False)

    class Meta:
        ordering =("name",)
