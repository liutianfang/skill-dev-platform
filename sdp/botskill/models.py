from django.db import models
import django.utils.timezone as timezone


'''
设备所有者，一般情况下是音箱所有者
'''

class BOT_DeviceOwner(models.Model):
    userid = models.CharField('userID',max_length = 256)
    create_time = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['pk']
        verbose_name = '设备所有者'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.userid

class BOT_Device(models.Model):
    deviceid = models.CharField('设备ID',max_length = 256)
    ownerid = models.ForeignKey(BOT_DeviceOwner, None, null=True)
    create_time = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['pk', "ownerid"]
        verbose_name = '设备ID'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.deviceid


'''
demo data, show user for DUEROS_Device,DUEROS_DeviceOwner

'''
class BOT_Whereis(models.Model):

    ownerid = models.ForeignKey(BOT_DeviceOwner, None, null=True)
    deviceid = models.ForeignKey(BOT_Device, None, null=True)

    input_itemname =models.CharField('输入物品名', max_length=256)
    input_position =models.CharField('输入位置', max_length=256)
    preposition=models.CharField('位置介词', max_length=16)
    create_time = models.DateTimeField(default=timezone.now)


    class Meta:
        ordering = ['pk']
        verbose_name = '在哪'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.ownerid.userid +": " + self.input_itemname +" 在 " + self.input_position +" "+ self.preposition

class BOT_Log(models.Model):
    request=models.TextField("请求")
    ip=models.CharField('IP', max_length=16)
    header=models.TextField("Header")
    response = models.TextField("响应")
    exmsg = models.CharField('自定义信息', max_length=1024)
    create_time = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['-pk']
        verbose_name = '日志'
        verbose_name_plural = verbose_name