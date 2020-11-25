from django.contrib import admin

## TODO : ask when to use ugettext and when to use gettext (what is different)
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext as _

from .models import User, Identity


class UserAdmin(BaseUserAdmin):
    ordering = ['id']
    list_display = ('email', 'first_name', 'last_name', 'is_staff')
    search_fields = ['email', 'first_name', 'last_name']
    readonly_fields = ('date_joined', 'last_login')
    fieldsets = (
        (None, {'fields': ('email', 'first_name', 'last_name', 'avatar', 'code', 'password')}),
        (_('important dates'), {'fields': ('date_joined', 'last_login')}),
    )


class IdentityAdmin(admin.ModelAdmin):
    ordering = ['id']
    list_display = ('request_time', 'expire_time', 'status')
    list_filter = ('user',)


admin.site.register(User, UserAdmin)
admin.site.register(Identity, IdentityAdmin)
