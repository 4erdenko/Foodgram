from django.contrib import admin
from django.contrib.admin import register

from users.models import Subscription, User


@register(User)
class UserAdmin(admin.ModelAdmin):
    """
    Admin model for User.

    Attributes:
        list_display (tuple): The fields to display in the list view.
        search_fields (tuple): The fields to search in the admin interface.
        list_filter (tuple): The fields to use for filtering in the admin
        interface.
    """

    def save_model(self, request, obj, form, change):
        if obj.pk:
            orig_obj = User.objects.get(pk=obj.pk)
            if obj.password != orig_obj.password:
                obj.set_password(obj.password)
        else:
            obj.set_password(obj.password)

        obj.save()

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


@register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    """
    Admin model for Subscription.

    Attributes:
        list_display (tuple): The fields to display in the list view.
        search_fields (tuple): The fields to search in the admin interface.
        list_filter (tuple): The fields to use for filtering in the admin
        interface.
        empty_value_display (str): The display value for empty fields.
    """

    list_display = ('follower', 'following')
    search_fields = ('follower', 'following')
    list_filter = ('follower', 'following')
    empty_value_display = '-пусто-'
