from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Topic, Ticket, Message, Attachment


class AttachInline(admin.TabularInline):
    model = Attachment
    extra = 1
    fieldsets = [
        (None, {'fields': ['file']})
        ]

class MessageInline(admin.StackedInline):
    model     = Message
    extra     = 1
    fieldsets = [
        (None, {'fields': ['user', 'rate', 'text']})
        ]

class TopicAdmin(admin.ModelAdmin):
    list_display  = ('creator', 'title', 'description', 'slug')
    search_fields = ['title', 'description', 'slug']
    list_filter   = []
    fieldsets     = [
        (None, {'fields': ['creator', 'title', 'description', 'slug', 'supporters']})
        ]

class TicketAdmin(admin.ModelAdmin):
    list_display  = ('creator', 'title', 'status', 'priority', 'creation_date', 'last_update')
    search_fields = ['title']
    list_filter   = ['status', 'priority', 'creation_date', 'last_update']
    fieldsets     = [
        (None, {'fields': ['creator', 'title', 'topic', 'status', 'priority']})
        ]
    inlines       = [MessageInline]

class MessageAdmin(admin.ModelAdmin):
    list_display  = ('user', 'ticket', 'text', 'rate')
    search_fields = ['text']
    list_filter   = ['date']
    inlines       = [AttachInline]

class AttachmentAdmin(admin.ModelAdmin):
    list_display  = ('message', 'file')
    list_filter   = []

admin.site.register(Topic, TopicAdmin)
admin.site.register(Ticket, TicketAdmin)
admin.site.register(Message, MessageAdmin)
admin.site.register(Attachment, AttachmentAdmin)
