from django.contrib import admin
from django.contrib.admin import register
from users.models import User


@register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'is_active',
        'username',
        'email',
    )
    search_fields = ('username', 'email')
    list_filter = (
        'is_active',
        'last_name',
        'email',
    )
