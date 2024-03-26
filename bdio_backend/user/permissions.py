# Permission.py file
# This file contains the permissions for the user model

from rest_framework.permissions import BasePermission

class IsTutor(BasePermission):
    """
    Permission for tutors
    """
    def has_permission(self, request, view):
        return request.user.is_tutor