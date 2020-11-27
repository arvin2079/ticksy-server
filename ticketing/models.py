from django.db import models
from users.models import User


class Topic(models.Model):
    creator     = models.ForeignKey(User, related_name='created_topics', blank=True, null=True, on_delete=models.CASCADE, verbose_name='سازنده')
    title       = models.CharField(max_length=100, verbose_name='موضوع')
    description = models.CharField(max_length=500, verbose_name='توضیحات')
    slug        = models.SlugField(max_length=50, unique=True, verbose_name='تگ آدرس')
    supporters  = models.ManyToManyField(User, blank=True, related_name='supported_topics', verbose_name='حمایت کنندگان')

    def __str__(self):
        return self.title

    class Meta:
        ordering= ['title']

class Ticket(models.Model):
    WAITING_FOR_ANSWER  = 1
    IN_PROGRESS         = 2
    ANSWERED            = 3
    CLOSED              = 4
    STATUS_CHOICES  = [
        (WAITING_FOR_ANSWER, 'در انتظار پاسخ'),
        (IN_PROGRESS, 'در حال پاسخ دهی'),
        (ANSWERED, 'جواب داده شده'),
        (CLOSED, 'بسته شده')
    ]

    HIGH    = 3
    AVERAGE = 2
    LOW     = 1
    PRIORITY_CHOICES = [
        (HIGH, 'اولویت زیاد'),
        (AVERAGE, 'اولویت متوسط'),
        (LOW, 'اولویت متوسط')
    ]
    
    creator         = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='آی دی سازنده تیکت')
    title           = models.CharField(max_length=100, verbose_name='موضوع')
    creation_date   = models.DateTimeField(auto_now_add=True, blank=True, null=True, verbose_name='زمان ایجاد')
    status          = models.IntegerField(choices=STATUS_CHOICES, default=WAITING_FOR_ANSWER, verbose_name='وضعیت')
    last_update     = models.DateTimeField(auto_now=True, blank=True, null=True, verbose_name='زمان آخرین تغییرات')
    priority        = models.IntegerField(choices=PRIORITY_CHOICES, verbose_name='اولویت')
    topic           = models.ForeignKey(Topic, on_delete=models.CASCADE, verbose_name='اطلاعات تیکت')

    def __str__(self):
        return self.title

    class Meta:
        ordering= ['title']
    
class Message(models.Model):
    user    = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='سازنده')
    ticket  = models.ForeignKey(Ticket, on_delete=models.CASCADE, verbose_name='اطلاعات تیکت')
    rate    = models.FloatField(blank=False, null=False, default=1, verbose_name='امتیاز')
    date    = models.DateTimeField(auto_now=False, auto_now_add=True, null=True, blank=True, verbose_name='زمان ایجاد')
    text    = models.TextField(blank=True, null=False, verbose_name='متن تیکت')

    def __str__(self):
        return self.text

    class Meta:
        ordering= ['id']

class Attachment(models.Model):
    message = models.ForeignKey(Message, on_delete=models.CASCADE, verbose_name='پیام')
    file    = models.FileField(upload_to='files/', blank=False, null=False, verbose_name='فایل')

    class Meta:
        ordering= ['id']
