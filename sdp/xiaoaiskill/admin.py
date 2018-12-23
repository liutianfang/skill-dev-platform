from django.contrib import admin

from django.contrib import admin
from xiaoaiskill.models import *


class MI_Whereis_LogAdmin(admin.ModelAdmin):
    list_display = ("pk",'create_time','request',"response","ip","exmsg",)


admin.site.register(MI_Log, MI_Whereis_LogAdmin)
admin.site.register(MI_Device)
admin.site.register(MI_DeviceOwner)