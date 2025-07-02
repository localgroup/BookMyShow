from django.urls import path, re_path
from . import views


urlpatterns = [
    path('showtime/<slug:slug>/', views.TheaterShowtimeView, name='theater_showtime'),
    # path('theater/<slug:slug>/<date_str>/', views.TheaterShowtimeView, name='theater_showtime_date'),
    re_path(r'^theater/(?P<slug>[-\w]+)/(?P<date_str>\d{4}-\d{2}-\d{2})/$', views.TheaterShowtimeView, name='theater_showtime_date'),
    path('theater/seat/<int:show_id>/', views.SeatSelectionView, name='seat_selection'),
    path('booking_ticket/<int:show_id>/', views.BookTicketView, name='booking_ticket'),
    
    
]