from django.shortcuts import render, get_object_or_404
from movies.models import Movie
from django.db.models import Avg, Sum, Count
from reviews.models import Review

# Create your views here.


def MovieView(request, slug):
    movie = Movie.objects.get(slug=slug)
    casts = movie.cast.all()
    average_rating = movie.reviews.aggregate(Avg('rating'))['rating__avg']
    
    return render(request, 'templates/dashboard/movie_detail.html', {
        'movie': movie,})