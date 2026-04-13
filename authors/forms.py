from django import forms
from django.core.exceptions import ValidationError
from .models import Author


class AuthorForm(forms.ModelForm):
    """ModelForm for creating and editing authors"""
    
    class Meta:
        model = Author
        fields = ['name', 'email', 'bio', 'photo', 'gender']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border border-slate-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-purple-500',
                'placeholder': 'Author Name'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'w-full px-4 py-3 border border-slate-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-purple-500',
                'placeholder': 'Email Address'
            }),
            'bio': forms.Textarea(attrs={
                'class': 'w-full px-4 py-3 border border-slate-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-purple-500',
                'placeholder': 'Author Biography',
                'rows': 4
            }),
            'photo': forms.FileInput(attrs={
                'class': 'w-full px-4 py-3 border border-slate-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-purple-500',
                'accept': 'image/*'
            }),
            'gender': forms.RadioSelect(attrs={
                'class': 'w-5 h-5'
            }),
        }
        help_texts = {
            'photo': 'Optional: Upload an author profile photo',
            'gender': 'Select your gender',
        }
    
    def clean_name(self):
        """Validate author name"""
        name = self.cleaned_data.get('name', '').strip()
        if not name:
            raise ValidationError('Author name is required.')
        return name
    
    def clean_email(self):
        """Validate author email"""
        email = self.cleaned_data.get('email', '').strip()
        if not email:
            raise ValidationError('Email is required.')
        
        # Check if email already exists (except when editing)
        existing = Author.objects.filter(email=email).exclude(pk=self.instance.pk).exists()
        if existing:
            raise ValidationError('An author with this email already exists.')
        return email
    
    def clean_bio(self):
        """Validate biography"""
        bio = self.cleaned_data.get('bio', '').strip()
        if not bio:
            raise ValidationError('Biography is required.')
        if len(bio) < 10:
            raise ValidationError('Biography must be at least 10 characters long.')
        return bio