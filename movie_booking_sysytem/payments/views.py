from django.shortcuts import render, redirect
from bookings.models import Booking
from django.conf import settings
import stripe
stripe.api_key = settings.STRIPE_SECRET_KEY
from payments.models import Payment

# Create your views here.

def PaymentView(request, booking_id):
    booking = Booking.objects.get(id=booking_id)
    if request.method == "POST":
        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[
                {
                    'price_data': {
                        'currency': 'inr',
                        'product_data': {
                            'name': 'Ticket Booking',
                        },
                        'unit_amount': int(booking.total_amount * 100),
                    },
                    'quantity': 1,
                },
            ],
            mode='payment',
            billing_address_collection='required',
            success_url=f'http://127.0.0.1:8000/payments/payment/success/{booking_id}/',
            cancel_url=f'http://127.0.0.1:8000/payments/payment/cancel/{booking_id}/',
        )
        return redirect(session.url, code=303)
    return render(request, 'payments/payment.html', 
                  {'stripe_public_key':settings.STRIPE_TEST_PUBLIC_KEY ,'booking': booking})
    
    
def PaymentSuccessView(request, booking_id):
    # Handle successful payment
    booking = Booking.objects.get(id=booking_id)
    booking.status = 'booked'
    booking.save()
    Payment.objects.create(
        booking=booking,
        amount=booking.total_amount,
        payment_method='card',
        status='successful'
        
    )
    
    return render(request, 'payments/success.html')


def PaymentCancelView(request, booking_id):
    # Handle cancelled payment
    booking = Booking.objects.get(id=booking_id)
    booking.status = 'cancelled'
    booking.save()
    Payment.objects.create(
        booking=booking,
        amount=booking.total_amount,
        payment_method='card',
        status='failed'
    )
    
    return render(request, 'payments/error.html')
    