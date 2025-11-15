# Django modules
from django.contrib.admin import register, ModelAdmin

# Project modules
from apps.auths.models import CustomUser

@register(CustomUser)
class CustomUserAdmin(ModelAdmin):
    """Admin class for CustomUser model"""
    list_display = (
        'email', 
        'username', 
        'is_staff', 
        'is_active',
    )
    search_fields = (
        'email', 
        'username',
    )
    list_filter = (
        'is_staff', 
        'is_active',
    )
    ordering = (
        'email',
    )
