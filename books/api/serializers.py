from rest_framework import serializers
from books.models import Book
from authors.models import Author

class AuthorNestedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ['id', 'name', 'email', 'bio', 'photo']
        read_only_fields = ['id']

class BookSerializer(serializers.ModelSerializer):
    authors = AuthorNestedSerializer(many=True, read_only=True)
    author_ids = serializers.PrimaryKeyRelatedField(
        queryset=Author.objects.all(),
        many=True,
        write_only=True,
        required=False,
        source='authors'
    )
    
    class Meta:
        model = Book
        fields = ['id', 'title', 'brief', 'price', 'no_of_page', 'image', 
                  'is_bestseller', 'authors', 'author_ids', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']
