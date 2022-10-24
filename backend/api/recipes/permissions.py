from rest_framework import permissions


class PatchIsAuthorOrReadAll(permissions.BasePermission):
    """Кастомный пермишенс. Читать могут все,
    изменять только автор или админ.
    """

    def has_permission(self, request, view):
        return bool(
            request.method in permissions.SAFE_METHODS
            or request.user and request.user.is_staff
            or request.user and request.user.is_authenticated
        )

    def has_object_permission(self, request, view, obj):
        return (
            request.user.is_staff
            or obj.author == request.user)
