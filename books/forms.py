from decimal import Decimal
from django import forms
from django.core.exceptions import ValidationError

from .models import Book
from authors.models import Author


class BookForm(forms.ModelForm):
    """
    ModelForm for creating and editing books.
    Handles Many-to-Many relationship with authors.
    """
    
    authors = forms.ModelMultipleChoiceField(
        queryset=Author.objects.all(),
        widget=forms.CheckboxSelectMultiple(attrs={
            'class': 'w-5 h-5'
        }),
        label='Select Author(s)',
        help_text='Select one or more authors for this book'
    )
    
    class Meta:
        model = Book
        fields = ['title', 'brief', 'price', 'no_of_page', 'image', 'is_bestseller', 'authors']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border border-slate-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-teal-500',
                'placeholder': 'Book Title'
            }),
            'brief': forms.Textarea(attrs={
                'class': 'w-full px-4 py-3 border border-slate-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-teal-500',
                'placeholder': 'Brief Description',
                'rows': 4
            }),
            'price': forms.NumberInput(attrs={
                'class': 'w-full px-4 py-3 border border-slate-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-teal-500',
                'placeholder': 'Price',
                'step': '0.01'
            }),
            'no_of_page': forms.NumberInput(attrs={
                'class': 'w-full px-4 py-3 border border-slate-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-teal-500',
                'placeholder': 'Number of Pages',
                'min': '1'
            }),
            'image': forms.FileInput(attrs={
                'class': 'w-full px-4 py-3 border border-slate-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-teal-500',
                'accept': 'image/*'
            }),
            'is_bestseller': forms.CheckboxInput(attrs={
                'class': 'w-5 h-5 text-teal-600 rounded focus:ring-2 focus:ring-teal-500'
            }),
        }
        help_texts = {
            'title': 'Enter the book title (must be unique)',
            'price': 'Price must be greater than 0',
            'no_of_page': 'Number of pages must be at least 1',
            'image': 'Upload a book cover image',
            'is_bestseller': 'Check this box if the book is a bestseller',
        }
    
    def __init__(self, *args, **kwargs):
        """
        Initialize form with optional book instance for editing.
        Makes image field optional when editing.
        """
        super().__init__(*args, **kwargs)
        
        # Image is only required when creating a new book (not editing)
        if self.instance.pk:
            self.fields['image'].required = False
    
    def clean_title(self):
        """Validate that title is unique and not empty"""
        title = self.cleaned_data.get('title', '').strip()
        
        if not title:
            raise ValidationError('Title cannot be empty.')
        
        # Check for duplicate title (case-insensitive)
        qs = Book.objects.filter(title__iexact=title)
        
        # Exclude current book when editing
        if self.instance.pk:
            qs = qs.exclude(pk=self.instance.pk)
        
        if qs.exists():
            raise ValidationError('A book with this title already exists.')
        
        return title
    
    def clean_brief(self):
        """Validate brief description"""
        brief = self.cleaned_data.get('brief', '').strip()
        
        if not brief:
            raise ValidationError('Description is required.')
        
        return brief
    
    def clean_price(self):
        """Validate price"""
        price = self.cleaned_data.get('price')
        
        if price and price <= 0:
            raise ValidationError('Price must be greater than 0.')
        
        return price
    
    def clean_no_of_page(self):
        """Validate number of pages"""
        no_of_page = self.cleaned_data.get('no_of_page')
        
        if no_of_page and no_of_page <= 0:
            raise ValidationError('Number of pages must be at least 1.')
        
        return no_of_page
    
    def clean_authors(self):
        """Validate that at least one author is selected"""
        authors = self.cleaned_data.get('authors')
        
        if not authors:
            raise ValidationError('Please select at least one author for this book.')
        
        return authors
