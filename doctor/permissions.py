

from rest_framework.permissions import BasePermission,SAFE_METHODS

class IsDoctor(BasePermission):
    def has_permission(self, request, view):
        if request.user and request.user.user_role == 'doctor':
            return True
        print(f"Permission denied for user: {request.user.user_role}")
        return False

class IsPatient(BasePermission):
    def has_permission(self, request, view):
        if request.user and request.user.user_role == 'patient':
            return True
        print(f"Permission denied for user: {request.user.user_role}")
        return False


class AllowAnyGet(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:  # SAFE_METHODS = ('GET', 'HEAD', 'OPTIONS')
            return True
        return request.user and request.user.is_authenticated


