from django.contrib import admin
from .models import FarmerProfile,Group

# Register your models here.


class FarmerProfileAdmin(admin.ModelAdmin):
    list_display = [
        'user',
        'nin'
        

    ]
    search_fields = ['user__username','nin']


admin.site.register(FarmerProfile, FarmerProfileAdmin)


class GroupAdmin(admin.ModelAdmin):
    list_display = [
        'name',
        'contact_person',
        'contact_person_phone',
        'contact_person_email',
        

    ]
    search_fields = ['name','contact_person']


admin.site.register(Group, GroupAdmin)

