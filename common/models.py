
from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext as _
import phonenumbers
from phonenumber_field.modelfields import PhoneNumberField
from common.choices import(GENDER_CHOICES)
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
# Create your models here.

class TimeStampedModel(models.Model):
    """
    Abstract model class that includes timestamp fields
    """
    created = models.DateTimeField(
        verbose_name=_('Created'),
        auto_now=True)
    modified = models.DateTimeField(
        verbose_name=_('Modified'),
        auto_now=True)

    # pylint: disable=too-few-public-methods
    class Meta:
        """
        Meta options for TimeStampedModel
        """
        abstract = True


class Region(models.Model):
    name = models.CharField(max_length=100, null=False, blank=False)

    def __str__(self):
        return self.name


class District(models.Model):
    name = models.CharField(max_length=100, null=False, blank=False)
    region = models.ForeignKey(Region, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class County(models.Model):
    name = models.CharField(max_length=100, null=False, blank=False)
    district = models.ForeignKey(District, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class SubCounty(models.Model):
    name = models.CharField(max_length=100, null=False, blank=False)
    county = models.ForeignKey(County, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Parish(models.Model):
    name = models.CharField(max_length=100, null=False, blank=False)
    sub_county = models.ForeignKey(SubCounty, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Village(models.Model):
    name = models.CharField(max_length=100, null=False, blank=False)
    parish = models.ForeignKey(Parish, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

#Extending the auth_user table
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    phone_number = PhoneNumberField(blank=False, null=False)
    phone_2 = PhoneNumberField(_('Phone number 2'), blank=True, null=True)
    home_address = models.TextField(max_length=100, blank=True)
    gender = models.CharField(choices=GENDER_CHOICES, max_length=15)
    profile_pic = models.ImageField(null=True, blank=True)
     # moved users location to profile to avoid redundancy
    region = models.ForeignKey(Region, on_delete=models.CASCADE, null=True, blank=False)
    district = models.ForeignKey(District, on_delete=models.CASCADE, null=True, blank=False)
    county = models.ForeignKey(County, on_delete=models.CASCADE, null=True, blank=False)
    sub_county = models.ForeignKey(SubCounty, on_delete=models.CASCADE, null=True, blank=False)
    parish = models.ForeignKey(Parish, on_delete=models.CASCADE, null=True, blank=False)
    village = models.ForeignKey(Village, on_delete=models.CASCADE, null=True, blank=False)


    def __str__(self):
        return '{} {}'.format(self.user.first_name, self.user.last_name)

    def get_full_name(self):
        return '{} {}'.format(self.user.first_name, self.user.last_name)