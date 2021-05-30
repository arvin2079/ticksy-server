from django.contrib import admin
from .models import Topic, Ticket, Message, Attachment, TicketHistory, Section, Admin


class AttachInline(admin.TabularInline):
    model = Attachment
    extra = 1


class MessageInline(admin.StackedInline):
    model = Message
    extra = 1
    show_change_link = True


class AdminAdmin(admin.ModelAdmin):
    list_display = ['title', 'topic']
    search_fields = ['title']
    autocomplete_fields = ['topic']

class TopicAdmin(admin.ModelAdmin):
    list_display = ('title', 'creator')
    search_fields = ['title', 'description', 'creator']
    list_filter = []
    filter_horizontal = ['admins']
    autocomplete_fields = ['creator']

class SectionAdmin(admin.ModelAdmin):
    list_display = ['title', 'topic', 'admin']
    search_fields = ['title', 'description']
    list_filter = ['topic']
    autocomplete_fields = ['topic', 'admin']


class TicketAdmin(admin.ModelAdmin):
    list_display = ('title', 'section', 'admin', 'get_status_display', 'get_priority_display', 'last_update')
    search_fields = ['title', 'creator']
    list_filter = ['status', 'priority', 'creation_date', 'last_update', 'topic']
    readonly_fields = ['creation_date', 'last_update']
    inlines = [MessageInline]
    autocomplete_fields = ['creator', 'topic', 'section']


class TicketHistoryAdmin(admin.ModelAdmin):
    list_display = ['ticket', 'admin', 'section', 'operator', 'date']
    search_fields = ['ticket', 'section', 'operator']
    list_filter = []
    readonly_fields = ['date']
    autocomplete_fields = ['ticket', 'admin', 'section', 'operator']


class MessageAdmin(admin.ModelAdmin):
    list_display = ('get_short_text', 'user', 'ticket', 'rate')
    search_fields = ['text', 'user']
    list_filter = ['date', 'rate']
    inlines = [AttachInline]
    readonly_fields = ['date']
    autocomplete_fields = ['user', 'ticket']


# class AttachmentAdmin(admin.ModelAdmin):
#     list_display  = ('message', 'file')
#     list_filter   = []

admin.site.register(Topic, TopicAdmin)
admin.site.register(Ticket, TicketAdmin)
admin.site.register(Message, MessageAdmin)
admin.site.register(Attachment)
admin.site.register(TicketHistory, TicketHistoryAdmin)
admin.site.register(Section, SectionAdmin)
admin.site.register(Admin, AdminAdmin)
# admin.site.register(Attachment, AttachmentAdmin)
