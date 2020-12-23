from django.db import models
from django.utils.translation import ugettext as _
from common .models import(TimeStampedModel,District,Region)
from django.contrib.auth.models import User
from common .choices import (TRANSACTION_TYPE,PAYMENT_OPTIONS, PAYMENT_MODE,YES_OR_NO,QUERIES, SCALE,SECTOR,
PROFESSION, EDUCATION_LEVEL,INCOME)
from geopy.geocoders import Nominatim
import phonenumbers
from phonenumber_field.modelfields import PhoneNumberField
from django_postgres_extensions.models.fields import ArrayField



# Create your models here.


class Sector(TimeStampedModel, models.Model):
   
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name



class Farm(TimeStampedModel, models.Model):
    FARM_STATUS = (
        (None, '--please select--'),
        ('active', 'Active'),
        ('closed', 'Closed')
     )
    farm_name = models.CharField(max_length=100, null=False, blank=False)
    farmer = models.ForeignKey('farmer.FarmerProfile', on_delete=models.CASCADE, related_name='farms')
    lat = models.FloatField(_('Latitude'), blank=True, null=True, help_text="Latitude of your location")
    lon = models.FloatField(_('Longitude'), blank=True, null=True,help_text="Longitude of your location")
    start_date = models.DateField(blank=False, null=False)
    close_date = models.DateField(blank=True, null=True)
    image = models.ImageField(null=True, blank=False)
    status = models.CharField(_('Farm Status'), default='active', max_length=20, choices=FARM_STATUS)
    general_remarks = models.TextField(null=True, blank=True)
    availability_of_services = models.BooleanField(_('Have access to Services ?.'), choices=YES_OR_NO, null=False, blank=False, default=True)
    availability_of_water = models.BooleanField(_('Does a the farm have a water source ?.'), choices=YES_OR_NO, null=False, blank=False, default=True)
    land_occupied = models.FloatField( _('Amount of land occupied(acres)'), blank=False, null=True)
    available_land = models.FloatField( _('Size of land Available'), blank=True, null=True)

    def __str__(self):
        return self.farm_name

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


class EnterpriseType(TimeStampedModel, models.Model):

    name = models.CharField(max_length=50, null=False, blank=False)
    sector = models.ForeignKey(Sector, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.name



class Enterprise(TimeStampedModel, models.Model):
    Enterprise_STATUS = (
        (None, '--please select--'),
        ('open', 'Open'),
        ('closed', 'Closed')
     )
    name = models.CharField(_('Enterprise Name'), max_length=50, null=False, blank=False)
    farm = models.ForeignKey(Farm, on_delete=models.CASCADE, null=True, related_name='enterprises')
    sector = models.ForeignKey(Sector, on_delete=models.CASCADE, null=True, blank=False)
    source = models.CharField(_('Source(Operation wealth creation, etc)'),blank=False, null=True, max_length=200)
    enterprise_type = models.CharField(blank=False, null=True, max_length=200)
    animal_seed_density = models.PositiveIntegerField(blank=True, null=True, verbose_name='Number of animals/seedling per enterprise in a particular period of time.')
    capital_invested = models.DecimalField(decimal_places=2, max_digits=1000, null=True)
    return_on_investment = models.DecimalField(_('Expected Return on Investment'), decimal_places=2, max_digits=1000, null=True)
    from_period = models.DateField(blank=False, null=True)
    to_period = models.DateField(blank=False, null=True)
    land_occupied = models.FloatField( blank=False, null=True)
    start_date = models.DateField(_('Farm Start Date'), blank=False, null=True)
    close_date = models.DateField(blank=True, null=True)
    description = models.TextField(null=True, blank=True)
    image = models.ImageField(null=True, blank=False)
    status = models.CharField(_('Enterprise Status'), default='active', max_length=20, choices=Enterprise_STATUS)


    def __str__(self):
        return self.name



class FarmFacility(TimeStampedModel, models.Model):
    name = models.CharField(max_length=100, null=False, blank=False)
    farm = models.ForeignKey(Farm, on_delete=models.DO_NOTHING, related_name='facilities')
    description = models.TextField( blank=True, null=True)
    image = models.ImageField()

    def __str__(self):
        return self.name

'''
These are farm products
'''
class Produce(TimeStampedModel, models.Model):
    name = models.CharField(max_length=100, null=False, blank=False)
    description = models.TextField( blank=True, null=True)
    quantity = models.DecimalField(decimal_places=2, max_digits=20, blank=False)

    def __str__(self):
        return self.name


class FarmProduce(TimeStampedModel, models.Model):
    enterprise = models.ForeignKey(Enterprise, on_delete=models.DO_NOTHING, null=False, blank=False, related_name='farm_produces')
    produce = models.ForeignKey(Produce, on_delete=models.DO_NOTHING)
    quantity = models.FloatField(blank=False, null=False)
    description = models.TextField( blank=True, null=True)
    production_date = models.DateField()
    taken_by = models.CharField(max_length=100, null=True, blank=True)
    reported_by = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.produce)


class FinancialRecord(TimeStampedModel, models.Model):
    FINANCIAL_OPTIONS = (
    (None, '--please select--'),
    ('full_payment', 'full payment'),
    ('installments', 'installments'),
    ('debt', 'debt')
    )
    enterprise = models.ForeignKey(Enterprise, on_delete=models.DO_NOTHING, null=False, blank=False, related_name='farm_financial_record')
    transaction_type = models.CharField(choices=TRANSACTION_TYPE, max_length=100, null=False)
    payment_mode = models.CharField(choices=FINANCIAL_OPTIONS, max_length=100, null=True)
    next_payment_date = models.DateField(null=True, blank=True)
    transaction_date = models.DateField(auto_now=True)
    spent_on = models.CharField(_('Payment for'),max_length=200)
    transaction_to = models.CharField(_('Payment To/From'),max_length=100)
    amount = models.FloatField(_('Amount paid'),blank=False, null=False)
    quantity = models.FloatField()
    means_of_payment = models.CharField(max_length=20, blank=False, null=False, choices=PAYMENT_MODE)
    transaction_date = models.DateField(auto_now=True)
    description = models.TextField( blank=True, null=True)
    reported_by = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.spent_on



class ProductionRecord(TimeStampedModel, models.Model):
    enterprise = models.ForeignKey(Enterprise, on_delete=models.DO_NOTHING, null=False, blank=False, related_name='farm_production_record')
    record_name = models.CharField(max_length=25, null=True, blank=True)
    production_activity = models.CharField(max_length=50, null=True, blank=True)
    quantity = models.DecimalField(decimal_places=2, max_digits=20, blank=False)
    measurements = models.CharField(max_length=25, null=True, blank=True)
    record_date = models.DateField()
    record_time = models.TimeField(auto_now=True, blank=True)
    record_taker = models.CharField(max_length=50, null=True, blank=True)
    general_remarks = models.TextField(max_length=150, null=True, blank=True)

    def __str__(self):
        return self.record_name

class Query(TimeStampedModel, models.Model):
    QUERY_TYPES = (
        (None, '--please select--'),
        ('extentional_reports', 'Extentional Report'),
        ('others', 'Others')
     )
    query_type = models.CharField(choices=QUERY_TYPES, max_length=25, null=True, blank=False)
    query_category = models.CharField(choices=QUERIES, max_length=25, null=True, blank=True)
    farm = models.ForeignKey(Farm, on_delete=models.DO_NOTHING, null=False, blank=False, related_name='farm_pests_and_diseases')
    name = models.CharField(_('Extension Workers Name'),max_length=50, null=True, blank=True)
    description = models.TextField( blank=True, null=True)
    date_discovered = models.DateField()
    action_taken = models.TextField( blank=False, null=True)
    image = models.ImageField(null=True, blank=False)
    reporting_date = models.DateField(auto_now=True)
    solution = models.TextField( blank=True, null=True)


    def __str__(self):
        return self.query_category


class RecordType(models.Model):
    name = models.CharField(max_length=100,null=False,blank=False)

    def __str__(self):
        return self.name


class FarmRecord(TimeStampedModel, models.Model):

    enterprise = models.ForeignKey(Enterprise, on_delete=models.DO_NOTHING, null=True, blank=False, related_name='farm_records')
    name = models.CharField(_('Activity'),max_length=200, null=False, blank=False)
    from_date = models.DateField()
    to_date = models.DateField()
    description = models.TextField( blank=True, null=True)
    # person responsible
    taken_by = models.CharField(_('Taken by'), blank=False, null=True, max_length=100)
    contact =  PhoneNumberField(_('Phone number'), blank=False, null=True)
    next_activity_date = models.DateField(null=True, blank=True)
    #reported_by = models.ForeignKey(User, on_delete=models.CASCADE)


    def __str__(self):
        return self.name


class Crop(models.Model):
    crop = models.CharField(max_length = 100, null= True, blank=False)
    benefits = models.CharField(max_length = 100, null=True, blank=True)
    what_you_need_to_know = models.CharField(max_length = 500, null=True, blank=True)
    required_capital = models. CharField(max_length=40, null = False, blank=True )

    def __str__(self):
        return self.crop


class Ecological_Zones(models.Model):
    ecological_zone_name = models.ForeignKey(Region,  on_delete=models.CASCADE, unique=False, related_name='zone', default=True)
    crops = models.ManyToManyField(Crop, related_name='ecological_zone_crops')



#Enterprise Selection
class EnterpriseSelection(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, unique=False, related_name='enterpriseselections')
    profession = models.CharField(_('What is your current proffession?'),max_length=200, choices = PROFESSION, null=False, default=False )
    monthly_income = models.CharField(null=True, choices=INCOME, max_length=200)
    level_of_education = models.CharField(max_length=100, choices =EDUCATION_LEVEL, null=False, default=False)
    capital = models.FloatField(_('How much money would you be willing to invest in farming?'), null=False, blank=False, default=True)
    what_is_your_inspiration_for_considering_in_farming = models.TextField(null=True, blank=True)
   # interested_sector = models.CharField(_('What Sector of farming are you interested in'), max_length = 100, choices=SECTOR, null=True, blank=False)
    scale = models.CharField(_('At what scale would you like to do farming?'), max_length = 100, choices=SCALE, null=True, blank=False)
    #Land
    own_piece_of_land = models.BooleanField(_('Do you own or have access to a piece of land to use for your farming activities'), choices=YES_OR_NO, null=False, blank=False, default=False)
    land_size = models.FloatField(_('What is the size of the land in acres'), null=True, default=False,blank=True)
    land_location = models.ForeignKey(District,  on_delete=models.CASCADE, unique=False, related_name='district', default=True)
    region = models.ForeignKey(Region,  on_delete=models.CASCADE, unique=False, related_name='region', default=False, help_text="What is your region of origin")
    involved_in_anyother_farming_activity = models.BooleanField(_('Have  you ever been involved in any farming activities'), choices=YES_OR_NO, null=False, blank=False, default=True)
    full_time_devotion = models.BooleanField(_('Do you want to devote full-time effort to the farm?'), choices=YES_OR_NO, null=False, blank=False, default=True)
    time_allocated_to_farming = models.FloatField(null= True, blank=True)
    rented_land = models.BooleanField(_('Do you intend to use rented land?'),choices=YES_OR_NO, null=False, blank=False, default=True)
    recommendation = models.ForeignKey(Ecological_Zones,  on_delete=models.CASCADE, unique=False, null=True,related_name='zone', default=True)


    def __str__(self):
        return str(self.recommendation)
