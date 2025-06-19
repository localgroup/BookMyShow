import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'movie_booking_sysytem.settings')
django.setup()

import requests
from datetime import datetime
from movies.models import Movie, Cast

# Python script to fetch movie data from OMDB API and populate the database

API_KEY = os.environ.get('OMDB_API_KEY') 
OMDB_API_URL = 'http://www.omdbapi.com/'

imdb_ids = [
    'tt3896198', 'tt4154796', 'tt1375666', 'tt7286456', 'tt0848228',
    'tt4154756', 'tt2975590', 'tt0468569', 'tt0111161', 'tt0120338'
]

for imdb_id in imdb_ids:
    params = {'i': imdb_id, 'apikey': API_KEY}
    response = requests.get(OMDB_API_URL, params=params)

    if response.status_code == 200:
        data = response.json()

        if data.get('Response') == 'True':
            title = data.get('Title')

            genre_list = data.get('Genre', '').split(', ')
            genre = genre_list[0] if genre_list else None

            language_list = data.get('Language', '').split(', ')
            language = language_list[0] if language_list else None

            synopsis = data.get('Plot')

            duration = int(data.get('Runtime', '0').replace(' min', '')) if data.get('Runtime') and data.get('Runtime') != 'N/A' else None

            release_date = None
            if data.get('Released') and data.get('Released') != 'N/A':
                try:
                    release_date = datetime.strptime(data.get('Released'), "%d %b %Y").date()
                except:
                    release_date = None

            status = 'Released' if release_date and release_date <= datetime.now().date() else 'Upcoming'

            trailer_url = f"https://www.imdb.com/title/{imdb_id}/"
            image_url = data.get('Poster') if data.get('Poster') != 'N/A' else None

            movie = Movie.objects.create(
                title=title,
                genre=genre,
                language=language,
                synopsis=synopsis,
                duration_minutes=duration,
                release_date=release_date,
                trailer_url=trailer_url,
                status=status,
                movie_image=image_url
            )

            print(f"✅ Added movie: {title}")

            actor_names = data.get('Actors', '').split(', ')
            for actor in actor_names:
                Cast.objects.create(movie=movie, name=actor)

            print(f"   🎭 Cast members added: {actor_names}")

        else:
            print(f"❌ API error for {imdb_id}: {data.get('Error')}")
    else:
        print(f"❌ HTTP error {response.status_code} for {imdb_id}")
