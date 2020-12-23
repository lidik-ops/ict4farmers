from django.contrib import admin
from .models import Region, District, County, SubCounty, Parish, Village,Profile

class RegionAdmin(admin.ModelAdmin):
    list_display = [
        'name'
        
   ]
    search_fields = ['name']
admin.site.register(Region, RegionAdmin)


class DistrictAdmin(admin.ModelAdmin):
    list_display = [
        'name',
        'region'
        
   ]
    search_fields = ['name', 'region__name']
admin.site.register(District, DistrictAdmin)


class CountyAdmin(admin.ModelAdmin):
    list_display = [
        'name',
        'district'
        
   ]
    search_fields = ['name', 'district__name']
admin.site.register(County, CountyAdmin)


class SubCountyAdmin(admin.ModelAdmin):
    list_display = [
        'name',
        'county'
        
   ]
    search_fields = ['name', 'county']
admin.site.register(SubCounty, SubCountyAdmin)



class ParishAdmin(admin.ModelAdmin):
    list_display = [
        'name',
        'sub_county'
        
   ]
    search_fields = ['name', 'sub_county']
admin.site.register(Parish, ParishAdmin)


class VillageAdmin(admin.ModelAdmin):
    list_display = [
        'name',
        'parish'
        
   ]
    search_fields = ['name', 'parish']
admin.site.register(Village, VillageAdmin)

class ProfileAdmin(admin.ModelAdmin):
    list_display = [
        'user',
        'phone_number',
        'gender',
        'home_address'
        
        
        
   ]
    search_fields = ['user__first_name','phone_number','gender']
admin.site.register(Profile, ProfileAdmin)