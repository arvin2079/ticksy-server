from django.core.validators import validate_slug, MaxValueValidator, MinValueValidator, FileExtensionValidator
from django.db import models
from users.models import User


class Topic(models.Model):
    creator     = models.ForeignKey(User, related_name='created_topics', on_delete=models.PROTECT, verbose_name='سازنده')
    title       = models.CharField(max_length=100, verbose_name='عنوان')
    description = models.TextField(verbose_name='توضیحات', null=True, blank=True)
    slug        = models.SlugField(max_length=30, unique=True, verbose_name='تگ آدرس', validators=[validate_slug], help_text='نام اینگلیسی مناسب برای لینک (به جای فاصله از خط تیره استفاده کنید)')
    supporters  = models.ManyToManyField(User, blank=True, related_name='supported_topics', verbose_name='پشتیبانان')

    def __str__(self):
        return self.title

    class Meta:
        ordering= ['title']
        verbose_name = 'بخش'
        verbose_name_plural = 'بخش ها'

    # todo: add a method to get links (for user and for supporters) of topic. [use 'reverse' from django rest, ask if google didn't answer]


WAITING_FOR_ANSWER  = '1'
IN_PROGRESS         = '2'
ANSWERED            = '3'
CLOSED              = '4'
STATUS_CHOICES  = [
    (WAITING_FOR_ANSWER, 'در انتظار پاسخ'),
    (IN_PROGRESS, 'در حال بررسی'),
    (ANSWERED, 'پاسخ داده شده'),
    (CLOSED, 'بسته شده')
]

HIGH    = '3'
AVERAGE = '2'
LOW     = '1'
PRIORITY_CHOICES = [
    (HIGH, 'اولویت زیاد'),
    (AVERAGE, 'اولویت متوسط'),
    (LOW, 'اولویت کم')
]


class Ticket(models.Model):
    creator         = models.ForeignKey(User, on_delete=models.PROTECT, verbose_name='سازنده')
    title           = models.CharField(max_length=100, verbose_name='عنوان')
    creation_date   = models.DateTimeField(auto_now_add=True, verbose_name='زمان ایجاد')
    status          = models.CharField(choices=STATUS_CHOICES, default=WAITING_FOR_ANSWER, verbose_name='وضعیت', max_length=1)
    last_update     = models.DateTimeField(auto_now=True, verbose_name='زمان آخرین تغییرات')
    priority        = models.CharField(choices=PRIORITY_CHOICES, verbose_name='اولویت', max_length=1)
    topic           = models.ForeignKey(Topic, on_delete=models.PROTECT, verbose_name='بخش مربوطه')

    def __str__(self):
        return self.title

    class Meta:
        ordering= ['-last_update']
        verbose_name = 'تیکت'
        verbose_name_plural = 'تیکت ها'
    
class Message(models.Model):
    user    = models.ForeignKey(User, on_delete=models.RESTRICT, verbose_name='فرستنده')
    ticket  = models.ForeignKey(Ticket, on_delete=models.CASCADE, verbose_name='تیکت مربوطه')
    rate    = models.PositiveIntegerField(blank=True, null=True, verbose_name='امتیاز', validators=[MaxValueValidator(5), MinValueValidator(1)])
    date    = models.DateTimeField(auto_now_add=True, verbose_name='زمان ایجاد')
    text    = models.TextField(verbose_name='متن تیکت')

    def __str__(self):
        return self.get_short_text()

    class Meta:
        ordering= ['-date']
        verbose_name = 'پیام'
        verbose_name_plural = 'پیام ها'

    def get_short_text(self):
        limit = 50
        return self.text[:limit] + ('...' if len(self.text) > limit else '')
    get_short_text.short_description = 'متن پیام'

class Attachment(models.Model):  # todo: if an Attachment object is deleted, the file of that object should delete too (u can write that code manually or download the appropriate package). [ask if u don't know how to do]
    message = models.ForeignKey(Message, on_delete=models.CASCADE, verbose_name='پیام مربوطه')

    VALID_FILE_EXTENSION = ['pdf', 'png', 'jpg', 'jpeg', 'zip', 'rar', 'mp4', 'mkv']
    file    = models.FileField(upload_to='files/', verbose_name='فایل', validators=[FileExtensionValidator(VALID_FILE_EXTENSION)])  # todo: add size validation (max 2 mg). [ask if u don't know how to add]

    class Meta:
        ordering= ['-id']
        verbose_name = 'فایل'
        verbose_name_plural = 'فایل ها'
