from rest_framework.permissions import BasePermission


class IsEditor(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user.is_authenticated and hasattr(request.user, 'writer') and request.user.writer.is_editor)
