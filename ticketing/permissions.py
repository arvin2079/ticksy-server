import datetime

from rest_framework import permissions
from users.models import IDENTIFIED


class IsIdentified(permissions.BasePermission):

    def has_permission(self, request, view):
        # try:
        #     print(request.user.username)
        #     user = User.objects.get(username=request.user.username)
        # except Exception as e:
        #     print(e)
        #     return False
        # if request.user.is_superuser:
        #     return True
        # if not request.user == user:
        #     print(1)
        #     return False
        # else:
        #     return True
        user = request.user

        # todo: remove button section after adding identity signal
        # -----------------------------
        if not hasattr(user, 'identity'):
            return False
        # -----------------------------

        return (user.identity.status == IDENTIFIED and (user.identity.expire_time > datetime.datetime.now() if user.identity.expire_time else True)) or user.is_superuser
