from django.contrib import admin
from .models import Author


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    """Admin interface for Author model"""
    list_display = ['name', 'email', 'created_at']
    search_fields = ['name', 'email']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Author Information', {
            'fields': ('name', 'email', 'bio', 'photo', 'gender')
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )