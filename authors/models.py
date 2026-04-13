from django.db import models
from django.core.exceptions import ValidationError

class Author(models.Model):
    """
    Author model for storing author information.
    - name: Author's full name (unique)
    - bio: Author's biography/description
    - photo: Author's profile photo
    - created_at: When the author was added
    """
    name = models.CharField(
        max_length=100,
        unique=True,
        help_text="Author's name must be unique"
    )
    bio = models.TextField(
        help_text="Author's biography"
    )
    email = models.EmailField(
        max_length=254,
        unique=True,
        error_messages={
            'required': 'Please provide your email address.',
            'unique': 'An account with this email already exists.',
        }
    )
    photo = models.ImageField(
        upload_to='authors/photos/',
        help_text="Author's profile photo",
        blank=True,
        null=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    
    updated_at = models.DateTimeField(auto_now=True)
    
    gender = models.CharField(max_length=20, choices=[('m', 'Male'), ('f', 'Female'), ('o', 'Other')], default='o' )
    class Meta:
        ordering = ['name']
        verbose_name = 'Author'
        verbose_name_plural = 'Authors'

    def clean(self):
        """Validate author fields"""
        errors = {}

        if not self.name or len(self.name.strip()) == 0:
            errors['name'] = 'Author name cannot be empty.'
            
        if not self.email or len(self.email.strip()) == 0:
            errors['email'] = 'Author email cannot be empty.'

        if not self.bio or len(self.bio.strip()) == 0:
            errors['bio'] = 'Author bio cannot be empty.'

        if len(self.bio.strip()) < 10:
            errors['bio'] = 'Author bio must be at least 10 characters.'
            
        

        if errors:
            raise ValidationError(errors)

    def save(self, *args, **kwargs):
        """Call clean before saving"""
        self.clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
