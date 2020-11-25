from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.utils.translation import ugettext_lazy as _


class UserManager(BaseUserManager):

    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('user must have email')
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password):
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save()
        return user


## TODO : ask if i should add "auto_now_add=True" to "last_login" ???

class User(PermissionsMixin, AbstractBaseUser):
    email = models.EmailField(unique=True, max_length=255)
    first_name = models.CharField(_('first name'), max_length=30, blank=True)
    last_name = models.CharField(_('last name'), max_length=30, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    date_joined = models.DateTimeField(_('date joined'), auto_now_add=True)
    last_login = models.DateTimeField(_('last login'), auto_now_add=True)
    avatar = models.ImageField(_('avatar'), upload_to='avatars/', blank=True, null=True)
    code = models.IntegerField(_('code'), blank=True, null=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'

    class Meta:
        ordering = ['date_joined']

    def __str__(self):
        return self.first_name + " " + self.last_name



ANONYMOUS = '0'
REQUESTED = '1'
IDENTIFIED = '2'
STATUS = (
    (ANONYMOUS, "تایید نشده"),
    (REQUESTED, "درخواست تایید"),
    (IDENTIFIED, "تایید شده"),
)

class Identity(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        unique=True
    )
    ## TODO : check that request_time should be read only, expire time can be editable
    identifier_image = models.ImageField(_('identifier image'), upload_to='Identifiers/', blank=True, null=True)
    request_time = models.DateTimeField(_('request time'), auto_now_add=True)
    expire_time = models.DateTimeField(_('expire time'))
    status = models.CharField(choices=STATUS, verbose_name='وضعیت کابری', max_length=1)

    class Meta:
        ordering = ['request_time']

    def __str__(self):
        return self.user.email + " : " + self.status
