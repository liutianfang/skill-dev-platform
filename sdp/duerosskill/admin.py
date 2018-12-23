from django.contrib import admin
from duerosskill.models import *
# Register your models here.

class Dueros_LogAdmin(admin.ModelAdmin):
    list_display = ('create_time','json_request',"response","ip","exmsg",)
    list_display_links=('create_time',)

admin.site.register(Dueros_Log, Dueros_LogAdmin)
admin.site.register(Dueros_Device)
admin.site.register(Dueros_DeviceOwner)