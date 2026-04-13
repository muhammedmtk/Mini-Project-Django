from django.shortcuts import get_object_or_404
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
from django.contrib import messages
from django.urls import reverse_lazy
from .forms import BookForm
from .models import Book


class BookListView(ListView):
    """Display all books"""
    model = Book
    template_name = 'books/index.html'
    context_object_name = 'books'
    paginate_by = 10
    
    def get_queryset(self):
        """Optimize query with prefetch_related for authors"""
        return Book.objects.prefetch_related('authors').all()


class BookCreateView(CreateView):
    """Create a new book"""
    model = Book
    form_class = BookForm
    template_name = 'books/create_book.html'
    success_url = reverse_lazy('books:index')
    
    def form_valid(self, form):
        """Handle successful form submission"""
        messages.success(self.request, 'Book created successfully!')
        return super().form_valid(form)


class BookDetailView(DetailView):
    """View a single book's details"""
    model = Book
    template_name = 'books/view_book.html'
    context_object_name = 'book'
    pk_url_kwarg = 'id'
    
    def get_queryset(self):
        """Optimize query with prefetch_related for authors"""
        return Book.objects.prefetch_related('authors')


class BookUpdateView(UpdateView):
    """Update an existing book"""
    model = Book
    form_class = BookForm
    template_name = 'books/edit_book.html'
    success_url = reverse_lazy('books:index')
    pk_url_kwarg = 'id'
    context_object_name = 'book'
    
    def form_valid(self, form):
        """Handle successful form submission"""
        messages.success(self.request, 'Book updated successfully!')
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        """Add book to context for template"""
        context = super().get_context_data(**kwargs)
        context['book'] = self.get_object()
        return context


class BookDeleteView(DeleteView):
    """Delete a book"""
    model = Book
    template_name = 'books/delete.html'
    success_url = reverse_lazy('books:index')
    pk_url_kwarg = 'id'
    context_object_name = 'book'
    
    def delete(self, request, *args, **kwargs):
        """Handle deletion and show success message"""
        messages.success(request, 'Book deleted successfully!')
        return super().delete(request, *args, **kwargs)

