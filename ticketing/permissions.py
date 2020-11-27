from rest_framework import permissions
from users.models import User


class Identified(permissions.BasePermission):

    def has_permission(self, request, view):
        try:
            print(request.user.username)
            user = User.objects.get(username=request.user.username)
        except Exception as e:
            print(e)
            return False
        if request.user.is_superuser:
            return True
        if not request.user == user:
            print(1)
            return False
        else:
            return True
