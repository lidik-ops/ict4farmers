from django.db import models
from django.contrib.auth.models import User, Group
from openmarket.models import Product
from phonenumber_field.modelfields import PhoneNumberField
from django.utils.translation import ugettext as _
from common .models import (District,County,Region,SubCounty, Parish,Village)
from common .models import TimeStampedModel
from farm .models import Sector


# Create your models here.
class AgentProfile(models.Model):
    SPECIFIC_ROLE = (
        (None, "--please select--"),
        ('account manager', 'Account Manager'),
        ('market manager', 'Market Manager'),
        ('call centre agent', 'Call Centre Agent'),
        ('notifications and alerts', 'Notifications and Alerts'),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='agent')
    contact = PhoneNumberField(blank=False)
    # agent address
    region = models.ForeignKey(Region, on_delete=models.CASCADE)
    district = models.ForeignKey(District, on_delete=models.CASCADE)
    specific_role = models.CharField(max_length = 50, choices=SPECIFIC_ROLE)

    def __str__(self):
        return self.specific_role


class Market(models.Model):
    market_name = models.CharField(max_length=100, blank = False)
    latitude = models.FloatField(_('Latitude'), blank=True, null=True)
    longitude = models.FloatField(_('Longitude'), blank=True, null=True)
    market_description = models.TextField(max_length=600, blank=False)

    def __str__(self):
        return self.market_name


class MarketPrice(TimeStampedModel, models.Model):
    market = models.ForeignKey(Market, blank = False, on_delete=models.CASCADE)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='unffeagent')
    product = models.ForeignKey(Product, blank=False, on_delete=models.CASCADE) # let it be product per price
    unit_of_measure = models.CharField(blank=False, max_length=100) # unit of measure like kilogram
    start_price = models.DecimalField(decimal_places=2, max_digits=20, blank=False)
    end_price = models.DecimalField(decimal_places=2, max_digits=20, blank=False)

    def __str__(self):
        return self.market



class Notice(TimeStampedModel, models.Model):
    # sector
    sector = models.ManyToManyField(Sector, related_name='notice_sectors', blank=True)
        # location
    region = models.ManyToManyField(Region, related_name='target_regions')
    district = models.ManyToManyField(District, related_name='notice_districts', blank=True)
    county = models.ManyToManyField(County, related_name='notice_counties', blank=True)
    sub_county = models.ManyToManyField(SubCounty, related_name='notice_sub_counties', blank=True)
    parish = models.ManyToManyField(Parish, related_name='notice_parishes', blank=True)
    village = models.ManyToManyField(Village, related_name='notice_villages', blank=True)
     
    # notice details
    notice_title = models.CharField(max_length=200, blank = False, null=False)
    display_up_to = models.DateTimeField(blank = False)
    posted_by = models.ForeignKey(User, on_delete=models.CASCADE)
    target_audience = models.ManyToManyField(Group, related_name='target_groups')
    description = models.TextField(max_length=300, blank=False)
  

    def __str__(self):
        return self.notice_title

# adding models for call response

class Call(TimeStampedModel, models.Model):
    session_id = models.CharField(primary_key=True,unique=True, max_length=200, null=False, blank=False)
    phone = PhoneNumberField(blank=False, null=True)
    call_date = models.DateTimeField(null=True, blank=True)
    call_type = models.CharField(max_length=200, null=True, blank=True)
    active = models.IntegerField(null=True)
    recording_url = models.URLField(null=True, blank=True)
    agent_phone = models.CharField(max_length=12, null=True, blank=True)
    call_duration = models.DurationField(null=True, blank=True)

    def __str__(self):
        return str(self.session_id)

# converstion record
class CallRsponse(TimeStampedModel, models.Model):
    QUESTION_TYPE=(
        (None, '--please select--'),
        ('enterprise','Enterprise Selection'),
        ('farmer','Farmer Information'),
        ('farm','Farm Information'),
        ('service providers','Service Providers'),
        ('services','Services'),
        ('open market','Open Market'),
        ('seller','Seller Information'),
        ('product','Products'),
        ('resource sharing','Resource Sharing'),
        ('alerts','Alerts and Opportunities'),
        ('weather','Micro Weather Services'),
        ('agents','UNFFE Agents')
    )
    call = models.OneToOneField(Call, on_delete=models.CASCADE, related_name='responses', null=True)
    agent = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    caller_name = models.CharField(_('Caller\'s Name'),max_length=200, null=True,blank=False)
    caller = PhoneNumberField(_('Phone Number'),blank=False, null=True)
    type_of_question =  models.CharField(max_length=50, null=True, blank=False, choices=QUESTION_TYPE)
    question = models.TextField(null=True)
    solution = models.TextField(null=True)
    called_from = models.ForeignKey(District, null=True, blank=False, on_delete=models.DO_NOTHING)

    def __str__(self):
        return str(self.type_of_question)