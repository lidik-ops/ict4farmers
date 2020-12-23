from django.db import models
from django.contrib.auth.models import User
from common.models import(Region, District, County, SubCounty, Parish, Village, TimeStampedModel)
from common.choices import(GENDER_CHOICES, MARITAL_STATUSES,STATUS, LAND_TYPES, SCALE, YES_OR_NO,EDUCATION_LEVEL)
import phonenumbers
from phonenumber_field.modelfields import PhoneNumberField
from django.utils.translation import ugettext as _
from farm .models import Sector

# Create your models here.

class Group(TimeStampedModel, models.Model):
    name = models.CharField(_('Group Name'), max_length=100, null=False, blank=False)
    description = models.TextField(blank=True, null=True)
    logo = models.ImageField(null=True)
    address = models.TextField(blank=False, null=False)
    contact_person = models.CharField(max_length=100)
    contact_person_email = models.EmailField(null=True)
    contact_person_phone = PhoneNumberField(blank=False, null=False)

    def __str__(self):
        return self.name


class FarmerProfile(TimeStampedModel, models.Model):
    CREDIT = (
        (None, '--please select--'),
        ('SACCO', 'SACCO'),
        ('Village Savings and Loan Associate', 'Village Savings and Loan Associate'),
        ('Bank', 'Bank'),
        ('Farmer Groups', 'Farmer Groups'),
     )

    user = models.OneToOneField(User, on_delete=models.CASCADE, unique=True, related_name='farmer',primary_key=True)
    # personal information

    nin = models.CharField(_('National Identity Number (NIN)'),max_length=14, null=False, blank=False)
    date_of_birth = models.DateField()
    level_of_education = models.CharField(choices = EDUCATION_LEVEL, max_length=100, null=False, blank=False)
    marital_status = models.CharField(choices=MARITAL_STATUSES, max_length=15, null=False, blank=False)
    number_of_dependants = models.PositiveIntegerField()
    credit_access = models.BooleanField(_('Have access to credit ?.'), choices=YES_OR_NO, null=True, blank=False)
    source_of_credit = models.CharField(choices=CREDIT, max_length=50, null=True, blank=False, default=False)
    experience = models.FloatField(_('Farming Experience in years'),null=False, blank=False)
    occupation = models.CharField(max_length=100, null=True, blank=False)
    # farming information
    sector = models.ManyToManyField(Sector, related_name='farmer_sectors')
    group = models.ForeignKey(Group, on_delete=models.DO_NOTHING, null=True, blank=True)
    size_of_land = models.DecimalField(_('Size of land in acres') ,decimal_places=2, max_digits=20, blank=False)
    type_of_land = models.CharField(choices=LAND_TYPES, max_length=20)
    production_scale = models.CharField(choices=SCALE, max_length=50)
    general_remarks = models.TextField(null=True, blank=True)
    # initial capital moved to farm
    #initial_total_capital = models.DecimalField(decimal_places=2, max_digits=20, blank=False)

    status = models.CharField(choices=STATUS, default='Pending', max_length=20,null=False)
    # handle approving of a farmer
    approver = models.ForeignKey(User, on_delete=models.DO_NOTHING,related_name="unffe_agent",null=True,blank=True)
    approved_date = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return str(self.user.last_name)



    class Meta:
        permissions = (
            ("can_approve_farmers", "Can approve farmers"),
        )

