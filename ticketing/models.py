from django.db import models
from users.models import User


class Topic(models.Model):
    creator     = models.ForeignKey(User, related_name='created_topics' , on_delete=models.CASCADE, verbose_name='سازنده')
    title       = models.CharField(max_length=100, blank=True, null=False, verbose_name='موضوع')
    description = models.CharField(max_length=500, blank=True, null=False, verbose_name='توضیحات')
    supporters  = models.ManyToManyField(User, related_name='supported_topics', verbose_name='حمایت کنندگان')
    slug        = models.SlugField(max_length=50, unique=True, blank=False, null=False, verbose_name='تگ آدرس')

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
    title           = models.CharField(max_length=100, blank=True, null=False, verbose_name='موضوع')
    creation_date   = models.DateTimeField(auto_now_add=True, auto_now=False, blank=True, null=False, verbose_name='زمان ایجاد')
    status          = models.CharField(max_length=1, choices=STATUS_CHOICES, default=WAITING_FOR_ANSWER, blank=False, null=False, verbose_name='وضعیت')
    last_update     = models.DateTimeField(auto_now=True, blank=True, null=False, verbose_name='آخرین زمان تغییرات')
    priority        = models.CharField(max_length=1, choices=PRIORITY_CHOICES, blank=False, null=False, verbose_name='اولویت')
    topic           = models.ForeignKey(Topic, on_delete=models.CASCADE, verbose_name='اطلاعات تیکت')

    def __str__(self):
        return self.title

    class Meta:
        ordering= ['title']
    
class Message(models.Model):
    user    = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='سازنده')
    ticket  = models.ForeignKey(Ticket, on_delete=models.CASCADE, verbose_name='اطلاعات تیکت')
    text    = models.TextField(blank=True, null=False, verbose_name='متن تیکت')
    date    = models.DateTimeField(auto_now=False, auto_now_add=True, null=False, blank=True, verbose_name='زمان ایجاد')
    rate    = models.SmallIntegerField(blank=False, null=False, default=1, verbose_name='امتیاز')

    def __str__(self):
        return self.text

    class Meta:
        ordering= ['id']

class Attachment(models.Model):
    message = models.ForeignKey(Message, on_delete=models.CASCADE, verbose_name='پیام')
    file    = models.FileField(upload_to='files/', blank=True, null=True, verbose_name='فایل')

    class Meta:
        ordering= ['id']
