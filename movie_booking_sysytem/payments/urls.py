from django.urls import path
from .import views



urlpatterns = [
    # path('pay/<int:booking_id>/', views.PaymentView, name='pay'),
    path('payment/<int:booking_id>/', views.PaymentView, name='pay'),  # Added this line
    path('payment/success/<int:booking_id>/', views.PaymentSuccessView, name='payment_success'),
    path('payment/cancel/<int:booking_id>/', views.PaymentCancelView, name='payment_cancel'),
]