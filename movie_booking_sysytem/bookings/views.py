from django.shortcuts import render, redirect
from movies.models import Movie
from theaters.models import Theater
from django.contrib import messages
from datetime import datetime, timedelta, date
from theaters.models import ShowTime, Seat
from django.contrib.auth.decorators import login_required
import json
from accounts.models import User
from bookings.models import Booking, BookingSeat
from django.shortcuts import HttpResponse
from django.conf import settings



def TheaterShowtimeView(request, slug, date_str=None):
    if date_str is None:
        selected_date = date.today()
        date_str = selected_date.strftime('%Y-%m-%d')
    else:
        try:
            selected_date = datetime.strptime(date_str, '%Y-%m-%d').date()
        except ValueError:
            messages.error(request, 'Invalid date format')
            return render(request, 'theaters/showtime.html', {})

    if not Movie.objects.filter(slug=slug).exists():
        messages.error(request, 'Invalid request')
        return render(request, 'theaters/showtime.html', {})

    movie = Movie.objects.get(slug=slug)
    

    theater_showtimes = []
    for theater in Theater.objects.all():
        if selected_date == date.today():
            showtime_qs = ShowTime.objects.filter(
                movie_name=movie,
                show_time__date=selected_date,
                show_time__time__gt=datetime.now().time(),
                theater=theater
            )
        else:
            showtime_qs = ShowTime.objects.filter(
                movie_name=movie,
                show_time__date=selected_date,
                theater=theater
            )

        if showtime_qs.exists():
            for showtime in showtime_qs:
                theater_showtimes.append({
                    'theater': theater,
                    'showtime': showtime
                })

    date_range = [selected_date + timedelta(days=i) for i in range(7)]

    context = {
        'movie': movie,
        'showtimes': theater_showtimes,
        'date_str': date_str,
        'date_range': date_range,
    }
    
    return render(request, 'theaters/showtime.html', context)


def SeatSelectionView(request, show_id):
    try:
        showtime = ShowTime.objects.get(id=show_id)
    except ShowTime.DoesNotExist:
        messages.error(request, 'Invalid showtime')
        return render(request, 'theaters/seat_selection.html', {})

    theater = showtime.theater
    movie = showtime.movie_name
    seats = Seat.objects.filter(theater=theater).order_by('-row_label', 'seat_number')
    seat_rows = {}
    booked_seats = [booking_seat.seat for booking_seat in BookingSeat.objects.filter(show_time=showtime)]
    for seat in seats:
        row = (seat.row_label,seat.seat_type)
        if row not in seat_rows:
            seat_rows[row] = []
        if seat not in booked_seats:
            seat_rows[row].append(seat)
        else:
            seat_rows[row].append(0)
            
    seat_types = ['Recliner', 'Gold', 'Silver']
    booked_seats_ids = [seat.id for seat in booked_seats]
            
    context = {
        'movie': movie,
        'theater': theater,
        'showtime': showtime,
        'seat_rows': seat_rows,
        'seat_types': seat_types,
        'booked_seats': booked_seats_ids,
        }
    
    return render(request, 'theaters/seat_selection.html', context)


@login_required
def BookTicketView(request, show_id):
    try:
        show_time = ShowTime.objects.get(id=show_id)
    except ShowTime.DoesNotExist:
        messages.error(request, 'Invalid showtime')
        return render(request, 'theaters/seat_selection.html', {})

    if request.method == 'POST':
        selected_seats = json.loads(request.POST['selected_seats'])
        # total_amount = eval(request.POST['total_amount'])
        total_amount = float(request.POST['total_amount'])
        tickets = []
        user = User.objects.get(username=request.user.username)
        convenience_fee = total_amount * 0.1
        sub_total = total_amount + convenience_fee
        
        if not selected_seats:
            messages.error(request, 'No seats selected')
            return render(request, 'theaters/seat_selection.html', {'show_time': show_time})

        booking = Booking.objects.create(
            user=user,
            show_time=show_time,
            total_amount=sub_total,
        )
        

        for seat in selected_seats:
            tickets.append(seat['key'])
            id = seat['id']
            seat_obj = Seat.objects.get(id=id)
            
            BookingSeat.objects.create(
                booking=booking, 
                seat=seat_obj,
                show_time=show_time
                )
            
        context = {
            'tickets': tickets,
            'convenience_fee': convenience_fee,
            'sub_total': sub_total,
            'total_amount': total_amount,
            'booking_time': Booking.objects.get(id=booking.id).booking_time,
            'booking': booking,
            'movie': show_time.movie_name,
            'stripe_public_key': settings.STRIPE_TEST_PUBLIC_KEY,
            'booking_id': booking.id,
        }
        
        messages.success(request, 'Booking confirmed successfully!')
        return render(request, 'bookings/booking_confirmation.html', context)

    return HttpResponse('Invalid request...')


