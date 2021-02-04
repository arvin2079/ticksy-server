# from rest_framework import permissions
# from .models import Identity, UNIDENTIFIED
#
#
# class IsUnidentified(permissions.BasePermission):
#
#     def has_permission(self, request, view):
#         user = request.user
#         identity = Identity.objects.filter(user=user).first()
#         return identity.status == UNIDENTIFIED
