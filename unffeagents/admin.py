from django.contrib import admin
from .models import Notice, AgentProfile

# Register your models here.
class NoticeAdmin(admin.ModelAdmin):
    list_display = [
        'notice_title',
        'created',
        'display_up_to',
        'posted_by',

        

    ]
    search_fields = ['notice_title','created']


admin.site.register(Notice, NoticeAdmin)

class AgentAdmin(admin.ModelAdmin):
    list_display = [
        'user',
        'contact',
            'region',
        'district',
        'specific_role'

    ]
    search_fields = ['user','specific_role','contact','district','region']


admin.site.register(AgentProfile, AgentAdmin)
