from datetime import datetime
from rest_framework import permissions
from users.models import IDENTIFIED
from rest_framework import status
from rest_framework.permissions import SAFE_METHODS


class IsIdentified(permissions.BasePermission):
    message = 'هویت شما هنوز توسط ادمین تایید نشده است.'
    status_code = status.HTTP_403_FORBIDDEN

    def has_permission(self, request, view):
        user = request.user
        if not hasattr(user, 'identity'):
            return False
        return (user.identity.status == IDENTIFIED and (user.identity.expire_time > datetime.now() if user.identity.expire_time else True)) or user.is_superuser


class IsOwner(permissions.BasePermission):
    message = 'شما سازنده این تاپیک نیستید.'
    status_code = status.HTTP_403_FORBIDDEN

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        if obj.creator == request.user:
            return True
        return False
