from django.urls import path
import accounts.views as views


urlpatterns = [
    path('register/', views.RegisterView, name='register'),
    path('signin/', views.LoginView, name='login'),
    path('home/', views.HomeView, name='home'),
    path('signout/', views.LogoutView, name='logout'),
    path('identify/', views.IdentifyUserView, name='identify_user'),
    path('verifyotp/<en_uname>/', views.OTPView, name='otp'),
]