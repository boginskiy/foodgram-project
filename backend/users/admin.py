from django.contrib import admin
from .models import User, UserFollowing


class UserAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'email', 'username', 'first_name', 'last_name', 'password')
    list_filter = ('email', 'username')


admin.site.register(User, UserAdmin)


class UserFollowingAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'subscriber', 'created')


admin.site.register(UserFollowing, UserFollowingAdmin)
