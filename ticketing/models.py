from django.core.validators import MaxValueValidator, MinValueValidator, FileExtensionValidator, \
    ValidationError
from django.template.defaultfilters import filesizeformat
from django.db.models.signals import pre_delete
from django.dispatch.dispatcher import receiver
from django.conf import settings
from django.db import models
from users.models import User


def topic_image_directory_path(instance, filename):
    return 'topic/{0}/image/{1}'.format(instance.creator.id, filename)


def section_image_directory_path(instance, filename):
    return 'topic/{0}/section/{1}/image/{2}'.format(instance.topic.creator.id, instance.topic.id, filename)


def user_files_directory_path(instance, filename):
    return 'user/{0}/files/{1}'.format(str(instance.message.user.email)[0:str(instance.message.user.email).index('@')],
                                       filename)


def validate_image_size(image):
    filesize = image.size
    if filesize > int(settings.MAX_UPLOAD_IMAGE_SIZE):
        raise ValidationError('حداکثر سایز عکس باید {} باشد'.format((filesizeformat(settings.MAX_UPLOAD_IMAGE_SIZE))))


VALID_AVATAR_EXTENSION = ['png', 'jpg', 'jpeg']

class Topic(models.Model):
    creator = models.ForeignKey(User, related_name='created_topics', null=True, on_delete=models.PROTECT,
                                verbose_name='سازنده')
    title = models.CharField(max_length=100, verbose_name='عنوان')
    description = models.TextField(verbose_name='توضیحات', null=True, blank=True)
    is_active = models.BooleanField(verbose_name='فعال', default=True,
                                    help_text='به جای حذف بخش، این گزینه را غیر فعال کنید')
    avatar = models.FileField(upload_to=topic_image_directory_path, null=True, blank=True,
                              validators=[FileExtensionValidator(VALID_AVATAR_EXTENSION), validate_image_size],
                              verbose_name='آواتار',
                              help_text='حداکثر سایز عکس باید {} باشد'.format(
                                  filesizeformat(settings.MAX_UPLOAD_IMAGE_SIZE)))
    is_recommended = models.BooleanField(verbose_name='پیشنهادی', default=False,
                                         help_text='در صورت فعال بودن این گزینه آدرس بخش مورد نظر در صفحه اصلی نمایش '
                                                   'داده خواهد شد')

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['title']
        verbose_name = 'بخش'
        verbose_name_plural = 'بخش ها'


@receiver(pre_delete, sender=Topic)
def topic_delete(sender, instance, **kwargs):
    instance.avatar.delete(False)


class Admin(models.Model):
    title = models.CharField(max_length=100, verbose_name='عنوان')
    topic = models.ForeignKey(to=Topic, on_delete=models.PROTECT, related_name='admins')
    users = models.ManyToManyField(to=User, blank=True, verbose_name='ادمین ها')

    def __str__(self):
        return self.title
    
    class Meta:
        ordering = ['title']
        verbose_name = 'ادمین'
        verbose_name_plural = 'ادمین ها'


WAITING_FOR_ANSWER = '1'
IN_PROGRESS = '2'
ANSWERED = '3'
CLOSED = '4'
STATUS_CHOICES = [
    (WAITING_FOR_ANSWER, 'در انتظار پاسخ'),
    (IN_PROGRESS, 'در حال بررسی'),
    (ANSWERED, 'پاسخ داده شده'),
    (CLOSED, 'بسته شده')
]

HIGH = '3'
AVERAGE = '2'
LOW = '1'
PRIORITY_CHOICES = [
    (HIGH, 'اولویت زیاد'),
    (AVERAGE, 'اولویت متوسط'),
    (LOW, 'اولویت کم')
]


class Section(models.Model):
    topic = models.ForeignKey(to=Topic, on_delete=models.PROTECT, verbose_name='متعلق به بخش')
    admin = models.ForeignKey(to=Admin, on_delete=models.RESTRICT, verbose_name='گروه مسئولین این زیربخش')
    title = models.CharField(max_length=100, verbose_name='عنوان')
    description = models.TextField(verbose_name='توضیحات', null=True, blank=True)
    is_active = models.BooleanField(verbose_name='فعال', default=True,
                                    help_text='به جای حذف زیر بخش، این گزینه را غیر فعال کنید')
    avatar = models.FileField(upload_to=section_image_directory_path, null=True, blank=True,
                              validators=[FileExtensionValidator(VALID_AVATAR_EXTENSION), validate_image_size],
                              verbose_name='آواتار',
                              help_text='حداکثر سایز عکس باید {} باشد'.format(
                                  filesizeformat(settings.MAX_UPLOAD_IMAGE_SIZE)))
    
    def __str__(self):
        return self.title
    
    class Meta:
        ordering = ['title']
        verbose_name = 'زیر بخش'
        verbose_name_plural = 'زیر بخش ها'


class Ticket(models.Model):
    creator = models.ForeignKey(User, on_delete=models.PROTECT, verbose_name='سازنده')
    title = models.CharField(max_length=100, verbose_name='عنوان')
    creation_date = models.DateTimeField(auto_now_add=True, verbose_name='زمان ایجاد')
    status = models.CharField(choices=STATUS_CHOICES, default=WAITING_FOR_ANSWER, verbose_name='وضعیت', max_length=1)
    last_update = models.DateTimeField(auto_now=True, verbose_name='زمان آخرین تغییرات')
    priority = models.CharField(choices=PRIORITY_CHOICES, verbose_name='اولویت', max_length=1)
    section = models.ForeignKey(to=Section, on_delete=models.PROTECT, verbose_name='زیر بخش مربوطه')
    admin = models.ForeignKey(to=Admin, on_delete=models.RESTRICT, verbose_name='ادمین ها')
    tags = models.TextField('تگ ها', blank=True, default='')

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-last_update']
        verbose_name = 'تیکت'
        verbose_name_plural = 'تیکت ها'


class TicketHistory(models.Model):
    ticket = models.ForeignKey(to=Ticket, on_delete=models.PROTECT, verbose_name='تیکت')
    admin = models.ForeignKey(to=Admin, on_delete=models.RESTRICT, verbose_name='ادمین')
    section = models.ForeignKey(to=Section, on_delete=models.PROTECT, verbose_name='زیر بخش')
    operator = models.ForeignKey(to=User, on_delete=models.PROTECT, verbose_name='ادمین مسئول')
    date = models.DateTimeField(verbose_name='زمان ایجاد', auto_now_add=True)

    def __str__(self):
        return str(self.id)
    
    class Meta:
        ordering = ['-date']
        verbose_name = 'تاریخچه تیکت'
        verbose_name_plural = 'تاریخچه تیکت ها'


class Message(models.Model):
    user = models.ForeignKey(User, on_delete=models.RESTRICT, verbose_name='فرستنده')
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE, verbose_name='تیکت مربوطه')
    rate = models.PositiveIntegerField(blank=True, null=True, verbose_name='امتیاز',
                                       validators=[MaxValueValidator(5), MinValueValidator(1)])
    date = models.DateTimeField(auto_now_add=True, verbose_name='زمان ایجاد')
    text = models.TextField(verbose_name='متن پیام')

    def __str__(self):
        return self.get_short_text()

    class Meta:
        ordering = ['-date']
        verbose_name = 'پیام'
        verbose_name_plural = 'پیام ها'

    def get_short_text(self):
        limit = 50
        return self.text[:limit] + ('...' if len(self.text) > limit else '')

    get_short_text.short_description = 'متن پیام'


def validate_file_size(file):
    filesize = file.size
    if filesize > int(settings.MAX_UPLOAD_FILE_SIZE):
        raise ValidationError('حداکثر سایز عکس باید {} باشد'.format((filesizeformat(settings.MAX_UPLOAD_FILE_SIZE))))


class Attachment(models.Model):
    message = models.ForeignKey(Message, on_delete=models.CASCADE, verbose_name='پیام مربوطه')

    VALID_FILE_EXTENSION = ['pdf', 'png', 'jpg', 'jpeg', 'zip', 'rar', 'mp4', 'mkv']
    attachmentfile = models.FileField(upload_to=user_files_directory_path, verbose_name='فایل',
                                      validators=[FileExtensionValidator(VALID_FILE_EXTENSION), validate_file_size],
                                      help_text='حداکثر سایز عکس باید {} باشد'.format(
                                          (filesizeformat(settings.MAX_UPLOAD_FILE_SIZE))))

    class Meta:
        ordering = ['-id']
        verbose_name = 'فایل'
        verbose_name_plural = 'فایل ها'


@receiver(pre_delete, sender=Attachment)
def attachment_delete(sender, instance, **kwargs):
    instance.attachmentfile.delete(False)
