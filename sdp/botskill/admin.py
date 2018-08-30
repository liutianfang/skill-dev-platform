from django.contrib import admin
from botskill.models import *
# Register your models here.


class BOT_LogAdmin(admin.ModelAdmin):
    list_display = ('create_time', 'request', "response", "ip", "exmsg",)


admin.site.register(BOT_Log, BOT_LogAdmin)
admin.site.register(BOT_Device)
admin.site.register(BOT_DeviceOwner)
admin.site.register(BOT_Whereis)
