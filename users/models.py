from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.utils.translation import ugettext_lazy as _


class UserManager(BaseUserManager):

    def create_user_identity(self, user):
        identity = Identity(user=user)
        identity.save()

    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('user must have email')
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save()
        self.create_user_identity(user)
        return user

    def create_superuser(self, email, password):
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save()
        self.create_user_identity(user)
        return user


## TODO : ask if i should add "auto_now_add=True" to "last_login" ???   No :))
## TODO: 1-add validators to fields and appropriate verbose_name. 2-add as much as you can fields and methods of AbstractUser (why didn't just override AbstractUser?).

class User(PermissionsMixin, AbstractBaseUser):
    email = models.EmailField(unique=True, max_length=255)
    first_name = models.CharField(_('first name'), max_length=30, blank=True)
    last_name = models.CharField(_('last name'), max_length=30, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    date_joined = models.DateTimeField(_('date joined'), auto_now_add=True)
    avatar = models.ImageField(_('avatar'), upload_to='avatars/', blank=True, null=True)
    code = models.IntegerField(_('code'), blank=True, null=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'

    class Meta:
        ordering = ['date_joined']

    def __str__(self):
        return self.first_name + " " + self.last_name


REQUESTED    = '1'
IDENTIFIED   = '2'
UNIDENTIFIED = '3'
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

    def __str__(self):
        return str(self.user) + ' ' + self.status

    class Meta:
        ordering = ['-request_time']
        verbose_name = 'احراز هویت'
        verbose_name_plural = 'احراز هویت'
