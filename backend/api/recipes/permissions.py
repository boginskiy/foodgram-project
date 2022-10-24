from rest_framework import permissions
from django.shortcuts import get_object_or_404
from recipes.models import Recipe


class PatchIsAuthorOrReadAll(permissions.BasePermission):
    """Кастомный пермишенс. Читать могут все,
    изменять только автор или админ.
    """

    def has_permission(self, request, view):

        info_url_pecipe_id = request.path.split('/')[-2]
        obj_recipe = get_object_or_404(Recipe, id=info_url_pecipe_id)

        return bool(
            request.method in permissions.SAFE_METHODS
            or request.user and request.user.is_staff
            or request.user == obj_recipe.author
        )
