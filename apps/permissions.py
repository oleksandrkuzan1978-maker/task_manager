from django.contrib.admindocs.views import user_has_model_view_permission
from rest_framework.permissions import BasePermission, SAFE_METHODS

class  IsSuperuserOrAuthenticatedReadOnly(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        return user.is_authenticated and (request.method in SAFE_METHODS or user.is_superuser)


class OnlyAdmin(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        return user.is_authenticated and user.is_superuser


# class StaffOrReadOnly(BasePermission):
#     def has_permission(self, request, view):
#         if request.method in SAFE_METHODS:
#             return True
#
#         return request.user.is_staff
        #return request.method in SAFE_METHODS or request.user.is_staff
