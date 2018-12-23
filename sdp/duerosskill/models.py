from django.db import models
import django.utils.timezone as timezone


class Dueros_DeviceOwner(models.Model):
    userid = models.CharField('userID', max_length=256)
    create_time = models.DateTimeField(default=timezone.now)
    infos = models.TextField("信息", default="{}", max_length=4096)  # 位置，json：{"p":["卧室","厨房"]}

    class Meta:
        ordering = ['pk']
        verbose_name = '设备所有者'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.userid


class Dueros_Device(models.Model):
    deviceid = models.CharField('设备ID', max_length=256)
    has_screen = models.BooleanField("是否有屏幕", default=False)
    ownerid = models.ForeignKey(Dueros_DeviceOwner, None, null=True)
    create_time = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['pk', "ownerid"]
        verbose_name = '设备ID'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.deviceid



class Dueros_Log(models.Model):

    json_request = models.TextField("请求", )
    bin_request=models.BinaryField("bin请求",null=True)
    ip = models.CharField('IP', max_length=16)
    header = models.TextField("Header")
    response = models.TextField("响应")
    exmsg = models.CharField('自定义信息', max_length=256)
    create_time = models.DateTimeField(default=timezone.now)
    intentid=models.IntegerField("意图",default=0,null=True)
    ownerid=models.ForeignKey(Dueros_DeviceOwner, None, null=True)
    deviceid=models.ForeignKey(Dueros_Device, None, null=True)

    #     status = models.CharField('状态', max_length=1, choices=STATUS_CHOICES, default='p')

    class Meta:
        ordering = ['-pk']
        verbose_name = '日志'
        verbose_name_plural = verbose_name

