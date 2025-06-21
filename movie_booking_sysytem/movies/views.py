from django.shortcuts import render, get_object_or_404
from movies.models import Movie
from django.db.models import Avg, Sum, Count
from reviews.models import Review

# Create your views here.


def MovieView(request, slug):
    movie = Movie.objects.get(slug=slug)
    casts = movie.cast.all()
    # rating = 
    # average_rating = Review.rating.aggregate(Avg('rating'))['rating__avg']
    # reviews = movie.reviews.all()
    return render(request, 'movies/movie_detail.html', {
        'movie': movie,
        'casts': casts,
        'average_rating': Review.objects.filter(movie=movie).aggregate(Avg('rating'))['rating__avg'],
        'total_reviews': Review.objects.filter(movie=movie).count(),
        'reviews': Review.objects.filter(movie=movie).order_by('-created_at'),
    })