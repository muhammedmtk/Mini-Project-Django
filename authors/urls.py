from django.urls import path
from . import views

app_name = 'authors'

urlpatterns = [
    path('', views.AuthorListView.as_view(), name='index'),
    path('create/', views.AuthorCreateView.as_view(), name='create'),
    path('<int:id>/view/', views.AuthorDetailView.as_view(), name='detail'),
    path('<int:id>/edit/', views.AuthorUpdateView.as_view(), name='edit'),
    path('<int:id>/delete/', views.AuthorDeleteView.as_view(), name='delete'),
]
