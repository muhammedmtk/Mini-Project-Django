from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from decimal import Decimal
from authors.models import Author

class Book(models.Model):
    title = models.CharField(
        max_length=255,
        unique=True,
        help_text="Book title must be unique"
    )
    brief = models.TextField(
        help_text="Brief description of the book"
    )
    image = models.ImageField(
        upload_to='books/covers/',
        help_text="Book cover image"
    )
    no_of_page = models.PositiveIntegerField(
        validators=[MinValueValidator(1)],
        help_text="Number of pages in the book"
    )
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal("0.01"))],
        help_text="Price must be greater than 0"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    authors = models.ManyToManyField(
        Author,
        related_name='books',
        blank=True,
        help_text="Select the book's author(s)"
    )
    is_bestseller = models.BooleanField(
        default=False,
        help_text="Mark as bestseller"
    )

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Book'
        verbose_name_plural = 'Books'

    def clean(self):
        """Validate model fields"""
        errors = {}

        # Validate title
        if not self.title or len(self.title.strip()) == 0:
            errors['title'] = 'Title must not be empty.'

        # Validate price
        if self.price and self.price <= 0:
            errors['price'] = 'Price must be greater than 0.'

        # Validate no_of_page
        if self.no_of_page <= 0:
            errors['no_of_page'] = 'Number of pages must be greater than 0.'

        # Validate brief
        if not self.brief or len(self.brief.strip()) == 0:
            errors['brief'] = 'Brief description must not be empty.'

        if errors:
            raise ValidationError(errors)

    def save(self, *args, **kwargs):
        """Call clean before saving"""
        self.clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title
    