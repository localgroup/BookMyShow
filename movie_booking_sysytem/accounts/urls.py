from django.urls import path
import accounts.views as views


urlpatterns = [
    path('register/', views.RegisterView, name='register'),
    path('login/', views.LoginView, name='login'),
    path('home/', views.HomeView, name='home'),
    path('logout/', views.LogoutView, name='logout'),
]