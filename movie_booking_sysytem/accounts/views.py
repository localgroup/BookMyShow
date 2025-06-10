from django.shortcuts import render
from .forms import RegisterForm, LoginForm
from django.core.mail import send_mail
from django.http import HttpResponse
from django.shortcuts import redirect
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required


# Create your views here.


def RegisterView(request):
    """
    View for user registration.
    Handles GET and POST requests to display and process the registration form.
    """
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            fname = form.cleaned_data.get('first_name')
            lname = form.cleaned_data.get('last_name')
            email = form.cleaned_data.get('email')
            message = f"Dear {fname} {lname}, you have successfully registered on bookmyshow."
            send_mail(
                subject='Registration Successful',
                message=message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[email],
                fail_silently=False,
            )
            messages.success(request, "Registration successful! A confirmation email has been sent to your email address.")
            return redirect('login')
    else:
        form = RegisterForm()
    
    return render(request, 'accounts/register.html', context={'form': form})


def LoginView(request):
    """
    View for user login.
    Handles GET and POST requests to display and process the login form.
    """
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, "Login successful!")
            return redirect('home')
            
        else:
            messages.error(request, "Invalid username or password.")
    else:
        form = LoginForm()
    
    return render(request, 'accounts/login.html', context={'form': form})


@login_required(login_url='login')
def HomeView(request):
    """
    View for the home page.
    Displays a welcome message to the user.
    """
    if request.user.is_authenticated:
        return render(request, 'accounts/home.html', context={'user': request.user})
    else:
        return redirect('login')
    
    
def LogoutView(request):
    """
    View for user logout.
    Logs out the user and redirects to the login page.
    """
    logout(request)
    messages.success(request, "You have been logged out successfully.")
    return redirect('login')