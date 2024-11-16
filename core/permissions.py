from rest_framework.permissions import BasePermission

class IsBankStaff(BasePermission):
    def has_permission(self, request, view):
        return request.user.role == "bank_staff"