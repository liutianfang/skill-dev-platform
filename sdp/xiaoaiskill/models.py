from django.db import models
import django.utils.timezone as timezone
import json
class MI_DeviceOwner(models.Model):
    userid = models.CharField('userID',max_length = 256)
    create_time = models.DateTimeField(default=timezone.now)
    extentions = models.CharField("扩展", default="{}", max_length=4096)

    class Meta:
        ordering = ['pk']
        verbose_name = '设备所有者'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.userid

class MI_Device(models.Model):
    deviceid = models.CharField('设备ID',max_length = 256)
    ownerid = models.ForeignKey(MI_DeviceOwner, None, null=True)
    create_time = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['pk']
        verbose_name = '设备ID'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.deviceid


class MI_Log(models.Model):
    request=models.TextField("请求")
    ip=models.CharField('IP', max_length=16)
    header=models.TextField("Header")
    response = models.TextField("响应")
    exmsg = models.CharField('自定义信息', max_length=256)
    create_time = models.DateTimeField(default=timezone.now)
    ownerid = models.ForeignKey(MI_DeviceOwner, None, null=True)
    deviceid = models.ForeignKey(MI_Device, None, null=True)


    class Meta:
        ordering = ['-pk']
        verbose_name = '日志'
        verbose_name_plural = verbose_name
