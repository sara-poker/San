from django.db import models
from django.db.models import Avg

from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager

from apps.setup.models import *

from config import settings


class Isp(models.Model):
    class Meta:
        verbose_name = 'اپراتور'
        verbose_name_plural = 'اپراتورها'

    CLOUD_CHOICE = (
        (True, 'True'),
        (False, 'False')
    )

    name = models.CharField(max_length=80, verbose_name='اسم')
    url = models.URLField(max_length=200, verbose_name='آدرس وب‌سایت', blank=True, null=True)
    org = models.CharField(max_length=100, verbose_name='سازمان', blank=True, null=True)
    country = models.ForeignKey(Country, verbose_name='کشور', on_delete=models.PROTECT, blank=True, null=True)
    as_number = models.CharField(max_length=50, verbose_name='AS')
    asname = models.CharField(max_length=100, verbose_name='AS Name')

    def __str__(self):
        return self.name

class App(models.Model):
    class Meta:
        verbose_name = 'نرم افزار'
        verbose_name_plural = 'نرم افزار ها'

    PLATFORM_CHOICE = (
        ('Android', 'Android'),
        ('Windows', 'Windows'),
        ('Web', 'Web'),
        ('Ios', 'Ios'),
        ('MacOS', 'MacOS')
    )

    CHOICE = (
        ('Free', 'Free'),
        ('Limited Free', 'Limited Free'),
        ('Non-free', 'Non-free')
    )

    name = models.CharField(verbose_name='اسم',max_length=100)
    platform = models.CharField(max_length=10, verbose_name='پلتفرم', choices=PLATFORM_CHOICE)
    maker = models.CharField(max_length=100, verbose_name='نام سازنده', blank=True, null=True)
    country = models.ForeignKey(Country, verbose_name='کشور سازنده', related_name='vpn_country',
                                    on_delete=models.PROTECT, blank=True, null=True)
    normal_user_fee = models.CharField(max_length=12, verbose_name='وضعیت رایگان بودن', choices=CHOICE, null=True,
                                           blank=True)

    def __str__(self):
        return self.name


class Test(models.Model):
    class Meta:
        verbose_name = 'تست سرعت'
        verbose_name_plural = 'تست های سرعت'

    STATUS_CHOICE = (
        ('Filter', 'Filter'),
        ('Without Filter', 'Without Filter')
    )

    date = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ تست', blank=True, null=True)

    city = models.CharField(verbose_name='شهر', max_length=140)
    app = models.ForeignKey(App, related_name='apps', on_delete=models.PROTECT)
    isp = models.ForeignKey(Isp, related_name='isps', on_delete=models.PROTECT)
    status = models.CharField(max_length=18, verbose_name='وضعیت', choices=STATUS_CHOICE)

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='کاربر')

    def __str__(self):
        return f"Test {self.app.name} by {self.user.name} in {self.date}"
