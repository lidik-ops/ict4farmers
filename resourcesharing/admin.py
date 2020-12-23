from django.contrib import admin
from .models import Resource
# Register your models here.

class ResourceAdmin(admin.ModelAdmin):
    list_display = [
        'resource_name',
        'owner',
        'Phone_number1',
        'Phone_number2',
        'resource_category',
        'lat',
        'lon',
        'terms_and_conditions',
        'resource_status',
        'available_from',
        'available_to',
        'image',
        'price'
        

    ]
    search_fields = ['resource_name','resource_category']


admin.site.register(Resource, ResourceAdmin)
