from django.contrib import admin
from .models import Seller, Product, ServiceProvider,Service,Category
from common.models import Region, District
from django import forms
#from .forms import ServiceProviderProfileForm
# Register your models here.


class SellerAdmin(admin.ModelAdmin):
    list_display = [
        'user',
]
    search_fields = ['seller_type', 'business_location']

admin.site.register(Seller, SellerAdmin)



class ProductAdmin(admin.ModelAdmin):
    list_display = [
       'name', 
       'enterprise', 
       'local_name', 
       'image', 
       'description', 
       'price', 
       'available',
       'date_created', 
       'date_updated'
        
]
    search_fields = ['name', 'slug']

admin.site.register(Product, ProductAdmin)

class ServiceProviderAdmin(admin.ModelAdmin):
    list_display = [
       'user'
]
    search_fields = ['user']

admin.site.register(ServiceProvider, ServiceProviderAdmin)

class ServiceAdmin(admin.ModelAdmin):
    list_display = [
       'service_name',  
       'lon', 
       'lat', 
       
       'availability_date', 
       'picture', 
        
]
admin.site.register(Service,  ServiceAdmin)

class CategoryAdmin(admin.ModelAdmin):
    list_display = [
       'cat_name'
       
]
admin.site.register(Category, CategoryAdmin)