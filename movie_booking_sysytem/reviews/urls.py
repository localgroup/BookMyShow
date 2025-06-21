from django.urls import path
from .views import views


urlpatterns = [
    path('add_review/<slug:slug>/', views.add_review, name='add_review'),
]