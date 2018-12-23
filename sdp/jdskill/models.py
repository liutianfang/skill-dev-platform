from django.db import models
import django.utils.timezone as timezone





class JD_DeviceOwner(models.Model):
    userid = models.CharField('userID',max_length = 256)
    create_time = models.DateTimeField(default=timezone.now)
    members=models.CharField("成员",default="{}", max_length=256)   #成员，json：{"m":["爸爸","妈妈"]}
    positions=models.CharField("位置",default="{}", max_length=4096)   #位置，json：{"p":["卧室","厨房"]}

    class Meta:
        ordering = ['pk']
        verbose_name = '设备所有者'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.userid

class JD_Device(models.Model):
    deviceid = models.CharField('设备ID',max_length = 256)
    ownerid = models.ForeignKey(JD_DeviceOwner, None, null=True)
    create_time = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['pk']
        verbose_name = '设备ID'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.deviceid


class JD_Log(models.Model):
    request=models.TextField("请求")
    ip=models.CharField('IP', max_length=32)
    header=models.TextField("Header")
    response = models.TextField("响应")
    exmsg = models.CharField('自定义信息', max_length=256)
    create_time = models.DateTimeField(default=timezone.now)
    deviceid = models.ForeignKey(JD_Device, None, null=True)
    ownerid = models.ForeignKey(JD_DeviceOwner, None, null=True)


    class Meta:
        ordering = ['-pk']
        verbose_name = '日志'
        verbose_name_plural = verbose_name