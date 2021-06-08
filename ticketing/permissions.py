from datetime import datetime
from rest_framework import permissions
from users.models import IDENTIFIED
from rest_framework import status


class IsIdentified(permissions.BasePermission):
    message = 'هویت شما هنوز توسط ادمین تایید نشده است.'
    status_code = status.HTTP_403_FORBIDDEN

    def has_permission(self, request, view):
        user = request.user
        if not hasattr(user, 'identity'):
            return False
        return (user.identity.status == IDENTIFIED and (
            user.identity.expire_time > datetime.now() if user.identity.expire_time else True)) or user.is_superuser


class IsOwner(permissions.BasePermission):
    message = 'شما سازنده این تاپیک نیستید.'
    status_code = status.HTTP_403_FORBIDDEN

    def has_object_permission(self, request, view, obj):
        if 'creator' in dir(obj):
            return obj.creator == request.user
        elif 'topic' in dir(obj):
            return obj.topic.creator == request.user
        return False


class IsTicketOwnerOrTopicOwner(permissions.BasePermission):
    message = 'شما سازنده یا ادمین این تیکت نیستید.'
    status_code = status.HTTP_403_FORBIDDEN

    def has_object_permission(self, request, view, obj):
        user = request.user
        if user == obj.ticket.topic.creator or user in obj.ticket.topic.supporters or user == obj.ticket.creator:
            return True
        return False


class IsSupporterOrOwnerOrTicketCreator(permissions.BasePermission):
    message = 'فقط سازنده های تیکت ها میتوانند به پیام ادمین ها رتبه دهند و برعکس.'
    status_code = status.HTTP_403_FORBIDDEN

    def has_object_permission(self, request, view, obj):
        user = request.user
        ticket = obj.ticket
        topic = ticket.topic
        return (((user == topic.creator or user in topic.supporters) and obj.user == ticket.creator) or (
            user == ticket.creator and (obj.user == topic.creator or obj.user in topic.supporters)))


class IsTicketAdmin(permissions.BasePermission):
    message = 'فقط یکی از ادمین های تیکت میتواند تیکت ها را تغییر دهد'
    status_code = status.HTTP_403_FORBIDDEN

    def has_object_permission(self, request, view, obj):
        return request.user in obj.admin.users.all()