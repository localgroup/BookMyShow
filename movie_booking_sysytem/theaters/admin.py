from django.contrib import admin
from .models import Theater, Seat, ShowTime

# Register your models here.


@admin.action(description="Generate Silver, Gold, Recliner seats")
def generate_all_seats(modeladmin, request, queryset):
    seat_plan = {
        'silver': {
            'rows': ['A', 'B', 'C'],
            'seats_per_row': 10
        },
        'gold': {
            'rows': ['D', 'E'],
            'seats_per_row': 8
        },
        'recliner': {
            'rows': ['F'],
            'seats_per_row': 6
        }
    }

    for theater in queryset:
        for seat_type, config in seat_plan.items():
            for row in config['rows']:
                for seat_no in range(1, config['seats_per_row'] + 1):
                    Seat.objects.get_or_create(
                        theater=theater,
                        row_label=row,
                        seat_no=seat_no,
                        seat_type=seat_type
                    )
        modeladmin.message_user(request, f"Seats added for {theater.name}")



@admin.register(Theater)
class TheaterAdmin(admin.ModelAdmin):
    list_display = ('name', 'city', 'address')
    ordering = ['name']
    actions = [generate_all_seats]


@admin.register(Seat)
class SeatAdmin(admin.ModelAdmin):
    list_display = ('theater', 'seat_number', 'row_label', 'seat_type')
    ordering = ['theater']
    
    
# admin.site.unregister(Seat)

@admin.register(ShowTime)
class ShowTimeAdmin(admin.ModelAdmin):
    list_display = ('theater', 'movie_name', 'show_time', 'silver_seats', 'gold_seats', 'platinum_seats')