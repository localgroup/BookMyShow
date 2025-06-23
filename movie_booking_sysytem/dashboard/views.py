from django.shortcuts import render, get_object_or_404
from .models import Movie
from reviews.views import add_review
from reviews.models import Review
from django.db.models import Avg, Sum, Count

# Create your views here.


def movie_dashboard(request):
    movies = Movie.objects.all().order_by('-release_date')
    return render(request, 'dashboard/dashboard.html', context={'movies': movies})


def movie_detail(request, slug):
    movie = get_object_or_404(Movie, slug=slug)
    rating_range = range(1, 11) 
    average_rating = movie.reviews.aggregate(Avg('rating'))['rating__avg']
    if (average_rating - int(average_rating)) > 0:
        average_rating = '{:.1f}'.format(average_rating)
    else:
        average_rating = int(average_rating)

    if request.method == 'POST':
        # Call add_review and pass the request and movie (or movie id/slug as needed)
        response = add_review(request, slug)
        if response:  # If add_review returns a redirect or response, return it
            return response

    return render(request, 'dashboard/detail.html', 
                  context={'movie': movie, 'rating_range': rating_range, 'average_rating': average_rating}
                  )



