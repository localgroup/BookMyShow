from django.urls import path
from . import views

# app_name = 'movies'

urlpatterns = [
    path('', views.movie_dashboard, name='movie_dashboard'),
    path('dashboard/<str:slug>/', views.movie_detail, name='movie_detail'),
]
