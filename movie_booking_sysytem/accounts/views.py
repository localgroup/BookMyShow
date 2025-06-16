from django.shortcuts import render
from .forms import RegisterForm, LoginForm
from django.core.mail import send_mail
from django.http import HttpResponse
from django.shortcuts import redirect
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from .models import User
from .forms import IdentifyForm
from django.utils import timezone
import datetime
from .utils import generate_otp, enc_uname, dec_uname


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
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
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


def IdentifyUserView(request):
    """
    View to identify the user.
    Returns a simple message with the user's username if authenticated.
    """
    
    if request.method == "POST":
        form = IdentifyForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            if User.objects.filter(username=username).exists():
                user = User.objects.get(username=username)
                otp = generate_otp()
                user.otp = otp
                user.otp_expiry = timezone.now() + datetime.timedelta(minutes=10)  # OTP valid for 10 minutes
                user.save()
                email = user.email
                # Send OTP to user's email
                send_mail(
                    subject='Your OTP Code',
                    message=f'Your OTP code is {otp}. It is valid for 10 minutes.',
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[email],
                    fail_silently=True,
                )
                messages.success(request, f"User {user.username} found. OTP sent to your registered email.")
                en_uname = enc_uname(username)
                url = f"{request.build_absolute_uri('/accounts/verifyotp/')}{en_uname}"
                # url = f"/accounts/verifyotp/{en_uname}/"
                return redirect(url)
            messages.error(request, "User not found.")
    
    else:
        form = IdentifyForm()
    return render(request, 'accounts/identify.html', context={'form': form})



def OTPView(request, en_uname):
    """
    View to handle OTP verification.
    This is a placeholder view; actual OTP logic should be implemented.
    """
    username = dec_uname(en_uname)
    if username and User.objects.filter(username=username).exists():
        if request.method == 'POST':
            otp_value = request.POST.get('otp')
            if otp_value is None or not otp_value.isdigit():
                messages.error(request, "Please enter a valid OTP.")
                return render(request, 'accounts/otp.html', context={'username': username})
            otp = int(otp_value)
            user = User.objects.get(username=username)
            if user.otp == otp and user.otp_expiry > timezone.now():
                user.otp_verified = True
                user.save()
                messages.success(request, "OTP verified successfully!")
                return redirect('home')
            else:
                messages.error(request, "Invalid OTP or OTP expired.")
                return render(request, 'accounts/otp.html', context={'username': username})
        else:
            # Render the OTP form for GET requests
            return render(request, 'accounts/otp.html', context={'username': username})
    messages.error(request, "Invalid or expired OTP link.")
    return redirect('login')
    return redirect('login')