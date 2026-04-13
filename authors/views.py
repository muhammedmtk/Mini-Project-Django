from django.shortcuts import get_object_or_404, redirect
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
from django.contrib import messages
from django.urls import reverse_lazy
from .forms import AuthorForm
from .models import Author


class AuthorListView(ListView):
    """Display all authors"""
    model = Author
    template_name = 'authors/index.html'
    context_object_name = 'authors_list'
    paginate_by = 10


class AuthorCreateView(CreateView):
    """Create a new author"""
    model = Author
    form_class = AuthorForm
    template_name = 'authors/author_form.html'
    success_url = reverse_lazy('authors:index')
    
    def form_valid(self, form):
        messages.success(self.request, 'Author created successfully!')
        return super().form_valid(form)


class AuthorDetailView(DetailView):
    model = Author
    template_name = 'authors/author_detail.html'
    context_object_name = 'author'
    pk_url_kwarg = 'id'
    
    def get_queryset(self):
        return Author.objects.prefetch_related('books')


class AuthorUpdateView(UpdateView):
    """Update an existing author"""
    model = Author
    form_class = AuthorForm
    template_name = 'authors/author_form.html'
    success_url = reverse_lazy('authors:index')
    pk_url_kwarg = 'id'
    
    def form_valid(self, form):
        messages.success(self.request, 'Author updated successfully!')
        return super().form_valid(form)


class AuthorDeleteView(DeleteView):
    model = Author
    template_name = 'authors/author_confirm_delete.html'
    success_url = reverse_lazy('authors:index')
    pk_url_kwarg = 'id'
    context_object_name = 'author'
    
    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Author deleted successfully!')
        return super().delete(request, *args, **kwargs)
