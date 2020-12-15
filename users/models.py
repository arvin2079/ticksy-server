from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    pass


REQUESTED   = '1'
IDENTIFIED  = '2'
UNIDENTIFIED= '3'
STATUS_CHOICES = (
    (IDENTIFIED, 'احراز شده'),
    (REQUESTED, 'درخواست احراز'),
    (UNIDENTIFIED, 'احراز نشده')
)

class Identity(models.Model):  # todo: should auto created with user.
    user                = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='کاربر')
    identifier_image    = models.ImageField(upload_to='pics/', blank=True, null=True, verbose_name='عکس پرسنلی')
    request_time        = models.DateTimeField(null=True, blank=True, verbose_name='زمان درخواست')
    expire_time         = models.DateTimeField(blank=True, null=True, verbose_name='زمان ابطال')
    status              = models.CharField(choices=STATUS_CHOICES, default=UNIDENTIFIED, verbose_name='وضعیت', max_length=1)

    class Meta:
        ordering=['-request_time']
        verbose_name = 'احراز هویت'
        verbose_name_plural = 'احراز هویت'
