from django.shortcuts import render
from .import models


# Create your views here.


def add_seat(request):
    if request.method == 'POST':
        theater_id = request.POST.get('theater_id')
        seat_number = request.POST.get('seat_number')
        row_label = request.POST.get('row_label')
        seat_type = request.POST.get('seat_type')

        # Create a new Seat instance
        seat = models.Seat(
            theater_id=theater_id,
            seat_number=seat_number,
            row_label=row_label,
            seat_type=seat_type
        )
        seat.save()

    theaters = models.Theater.objects.all()
    return render(request, 'add_seat.html', {'theaters': theaters})