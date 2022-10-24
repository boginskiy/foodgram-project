from django.contrib import admin
from .models import User, UserFollowing


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    """Настройка админки для User."""

    list_display = (
        'id', 'email', 'username', 'first_name', 'last_name', 'password')
    list_filter = ('email', 'username')
    search_fields = ('username', 'email')


@admin.register(UserFollowing)
class UserFollowingAdmin(admin.ModelAdmin):
    """Настройка админки для подписчиков."""

    list_display = ('id', 'user', 'subscriber', 'created')
