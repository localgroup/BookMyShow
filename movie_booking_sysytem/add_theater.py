import os
import django

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'movie_booking_sysytem.settings')
django.setup()

from theaters.models import Theater

# List of theaters to add
theaters = [
    {
        'name': 'PVR Orion Mall',
        'city': 'Bangalore',
        'address': 'Orion Mall, Rajajinagar, Bangalore'
    },
    {
        'name': 'INOX Garuda Mall',
        'city': 'Bangalore',
        'address': 'Garuda Mall, Magrath Road, Bangalore'
    },
    {
        'name': 'Urvashi Theater',
        'city': 'Bangalore',
        'address': 'Lalbagh Road, Bangalore'
    },
    {
        'name': 'PVR Vega City',
        'city': 'Bangalore',
        'address': 'Vega City Mall, Bannerghatta Road, Bangalore'
    },
    {
        'name': 'Cinepolis Royal Meenakshi Mall',
        'city': 'Bangalore',
        'address': 'Royal Meenakshi Mall, Bannerghatta Road, Bangalore'
    },
    {
        'name': 'Forum Mall PVR',
        'city': 'Bangalore',
        'address': 'Forum Mall, Koramangala, Bangalore'
    },
    {
        'name': 'PVR Phoenix Marketcity',
        'city': 'Bangalore',
        'address': 'Phoenix Marketcity Mall, Whitefield Road, Bangalore'
    },
    {
        'name': 'Gopalan Cinemas',
        'city': 'Bangalore',
        'address': 'Gopalan Innovation Mall, Bannerghatta Road, Bangalore'
    },
    {
        'name': 'Rex Theater',
        'city': 'Bangalore',
        'address': 'Brigade Road, Bangalore'
    },
    {
        'name': 'Cinepolis Binnypet',
        'city': 'Bangalore',
        'address': 'ETA Mall, Binnypet, Bangalore'
    }
]

# Insert into DB
for theater_data in theaters:
    Theater.objects.create(
        name=theater_data['name'],
        city=theater_data['city'],
        address=theater_data['address']
    )

print("✅ 10 Bangalore theaters added successfully.")
