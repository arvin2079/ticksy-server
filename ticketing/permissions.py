from datetime import datetime
from rest_framework import permissions
from rest_framework.generics import get_object_or_404

from ticketing.models import Topic, Ticket
from users.models import IDENTIFIED, User
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
        return request.method in permissions.SAFE_METHODS or request.user == obj.creator


class IsTopicOwnerOrSupporter(permissions.BasePermission):
    message = 'شما سازنده این تاپیک نیستید.'
    status_code = status.HTTP_403_FORBIDDEN

    def has_permission(self, request, view):
        topic = get_object_or_404(Topic, id=view.kwargs.get('id'))
        if request.method in permissions.SAFE_METHODS:
            return request.user == topic.creator or topic.admins.filter(users__in=[request.user.id]).exists()
        return request.user == topic.creator


class HasAccessToRoll(permissions.BasePermission):

    def has_permission(self, request, view):
        topic = get_object_or_404(Topic, id=view.kwargs['id'], is_active=True)
        if request.method == "GET":
            topic_members = User.objects.filter(admin__topic=topic).distinct()
            return (request.user in topic_members) or request.user == topic.creator
        return request.user == topic.creator


class IsTicketAdminOrCreator(permissions.BasePermission):
    message = 'شما سازنده یا ادمین این تیکت نیستید.'
    status_code = status.HTTP_403_FORBIDDEN

    def has_permission(self, request, view):
        ticket = get_object_or_404(Ticket, id=view.kwargs['id'])
        return ticket.creator == request.user or ticket.admin.users.filter(id=request.user.id).exists()

    # def has_object_permission(self, request, view, obj):
    #     user = request.user
    #     if user == obj.ticket.topic.creator or user in obj.ticket.topic.supporters or user == obj.ticket.creator:
    #         return True
    #     return False


class IsSupporterOrOwnerOrTicketCreator(permissions.BasePermission):
    message = 'فقط سازنده های تیکت ها میتوانند به پیام ادمین ها رتبه دهند و برعکس.'
    status_code = status.HTTP_403_FORBIDDEN

    def has_object_permission(self, request, view, obj):
        user = request.user
        ticket = obj.ticket
        topic = ticket.section.topic
        return (((user == topic.creator or user in topic.supporters) and obj.user == ticket.creator) or (
            user == ticket.creator and (obj.user == topic.creator or obj.user in topic.supporters)))


class HasChangeTicketPermission(permissions.BasePermission):
    message = 'فقط یکی از ادمین های تیکت میتواند تیکت ها را تغییر دهد'
    status_code = status.HTTP_403_FORBIDDEN

    def has_permission(self, request, view):
        ticket = get_object_or_404(Ticket, id=view.kwargs['id'])
        return request.method in permissions.SAFE_METHODS or ticket.admin.users.filter(id=request.user.id).exists()

    # def has_object_permission(self, request, view, obj):
    #     return request.user in obj.admin.users.all()