from django.contrib import admin
from .models import Theater, Seat

# Register your models here.

@admin.register(Theater)
class TheaterAdmin(admin.ModelAdmin):
    list_display = ('name', 'city', 'address')


@admin.register(Seat)
class SeatAdmin(admin.ModelAdmin):
    list_display = ('theater', 'seat_number', 'row_level', 'seat_type')
    
    
# admin.site.unregister(Seat)