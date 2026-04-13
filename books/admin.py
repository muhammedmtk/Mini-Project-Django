from django.contrib import admin
from .models import Book


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    """Book model admin with Many-to-Many author relationship"""
    list_display = ('title', 'price', 'no_of_page', 'is_bestseller', 'created_at')
    list_filter = ('is_bestseller', 'created_at', 'price', 'authors')
    search_fields = ('title', 'brief', 'authors__name')
    readonly_fields = ('created_at', 'updated_at')
    ordering = ('-created_at',)
    
    fieldsets = (
        ('Book Information', {
            'fields': ('title', 'brief', 'image', 'price')
        }),
        ('Details', {
            'fields': ('no_of_page', 'is_bestseller')
        }),
        ('Authors', {
            'fields': ('authors',),
            'description': 'Select one or more authors for this book. Authors are managed separately in the Author section.'
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
