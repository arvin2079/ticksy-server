from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    pass

class Identity(models.Model):
    REQUESTED   = 1
    IDENTIFIED  = 2
    UNIDENTIFIED= 3
    STATUS_CHOICES = [
        (IDENTIFIED, 'Identified'),
        (REQUESTED, 'Requested'),
        (UNIDENTIFIED, 'Unidentified')
    ]
    user                = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='کاربر')
    identifier_image    = models.ImageField(upload_to='pics/', blank=True, null=True, verbose_name='عکس پرسنلی')
    request_time        = models.DateTimeField(auto_now=False, auto_now_add=True, blank=True, verbose_name='زمان درخواست')
    expire_time         = models.DateTimeField(auto_now=False, auto_now_add=False, blank=True, null=True, verbose_name='زمان ابطال')
    status              = models.IntegerField(choices=STATUS_CHOICES, default=REQUESTED, blank=True, verbose_name='وضعیت')

    class meta:
        ordering=['user']