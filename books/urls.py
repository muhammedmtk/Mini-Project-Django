from django.urls import path
from . import views

app_name = 'books'

urlpatterns = [
    path('', views.BookListView.as_view(), name='index'),
    path('create/', views.BookCreateView.as_view(), name='create'),
    path('<int:id>/view/', views.BookDetailView.as_view(), name='detail'),
    path('<int:id>/edit/', views.BookUpdateView.as_view(), name='edit'),
    path('<int:id>/delete/', views.BookDeleteView.as_view(), name='delete'),
]