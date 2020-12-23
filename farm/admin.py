from django.contrib import admin
from .models import (Sector, Enterprise,Farm,EnterpriseType, Query,RecordType,EnterpriseSelection,
 FarmRecord, Ecological_Zones,Crop)
# Register your models here.

class SectorAdmin(admin.ModelAdmin):
    list_display = [
        'name'

    ]
    search_fields = ['name']


admin.site.register(Sector, SectorAdmin)

class QueryAdmin(admin.ModelAdmin):
    list_display = [
        'query_type',
        'query_category',
        'farm',
        'name',
        'description',
        'date_discovered',
        'action_taken',
        'image',
        'reporting_date',
        'solution'
        

    ]
    search_fields = ['name','size']


admin.site.register(Query, QueryAdmin)

class EnterpriseAdmin(admin.ModelAdmin):
    list_display = [
        'name',
        'farm',
        'description'
        

    ]
    search_fields = ['name','sector','description']


admin.site.register(Enterprise, EnterpriseAdmin)

class EnterpriseTypeAdmin(admin.ModelAdmin):
    list_display = [
        'name',
        'sector',
        

    ]
    search_fields = ['name','sector__name']


admin.site.register(EnterpriseType, EnterpriseTypeAdmin)

class FarmAdmin(admin.ModelAdmin):
    list_display = [
        'farm_name',
        'farmer',
        'start_date',
        'close_date',
        'status',
        'lat',
        'lon',
        'availability_of_services',
        'availability_of_water',
        'land_occupied'
        

    ]
    search_fields = ['farm_name','status','lat','lon']


admin.site.register(Farm, FarmAdmin)
admin.site.register(RecordType)
class FarmRecordAdmin(admin.ModelAdmin):
    list_display = [
        'enterprise',
        'name',
        'from_date',
        'to_date',
        'taken_by',
        

    ]
    search_fields = ['enterprise__name','record_type__name','name','taken_by']
admin.site.register(FarmRecord, FarmRecordAdmin)
class EnterpriseSelectionAdmin(admin.ModelAdmin):
    list_display = [
        'user',
        'profession',
        'monthly_income',
        'land_location',
        
    ]
    search_fields = ['user','land_location']

admin.site.register(EnterpriseSelection, EnterpriseSelectionAdmin)
class EcologicalZonesAdmin(admin.ModelAdmin):
  list_display = [
        'ecological_zone_name',
     
    ]
admin.site.register(Ecological_Zones,EcologicalZonesAdmin)

class CropAdmin(admin.ModelAdmin):
    list_display = [
        'crop',
    ]
admin.site.register(Crop, CropAdmin)
