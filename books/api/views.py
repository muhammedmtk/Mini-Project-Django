from rest_framework import viewsets
from books.models import Book
from .serializers import BookSerializer

class BookViewSet(viewsets.ModelViewSet):
    serializer_class = BookSerializer  
    def get_queryset(self):
        return Book.objects.prefetch_related('authors').all()

