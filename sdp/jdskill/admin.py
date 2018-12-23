from django.contrib import admin
from jdskill.models import *
# Register your models here.


class JD_LogAdmin(admin.ModelAdmin):
    list_display = ('create_time', 'request', "response", "ip", "exmsg",)
    list_display_links=('create_time',)


admin.site.register(JD_Log, JD_LogAdmin)
admin.site.register(JD_Device)
admin.site.register(JD_DeviceOwner)