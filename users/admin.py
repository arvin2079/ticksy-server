from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Identity


class IdentityAdmin(admin.ModelAdmin):
    list_display = ('user', 'status', 'request_time', 'expire_time')
    list_filter  = ['status', 'request_time', 'expire_time']
    search_fields = ['user']
    # fieldsets     = [
    #     (None, {'fields': ['user', 'identifier_image', 'status', 'expire_time']})
    #     ]

admin.site.register(User, UserAdmin)
admin.site.register(Identity, IdentityAdmin)