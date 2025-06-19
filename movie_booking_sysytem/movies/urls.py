from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.movie_dashboard, name='movie_dashboard'),
    path('dashboard/<int:movie_id>/', views.movie_detail, name='movie_detail'),
]
