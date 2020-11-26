from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Topic, Ticket, Message, Attachment


admin.site.register(Topic)
admin.site.register(Ticket)
admin.site.register(Message)
admin.site.register(Attachment)
