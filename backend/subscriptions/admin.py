from django.contrib import admin
from django.contrib.admin import register
from .models import Subscription


@register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('follower', 'following')
    search_fields = ('follower', 'following')
    list_filter = ('follower', 'following')
    empty_value_display = '-пусто-'
