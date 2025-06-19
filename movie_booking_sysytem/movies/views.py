from django.shortcuts import render, get_object_or_404
from .models import Movie

# Create your views here.


def movie_dashboard(request):
    movies = Movie.objects.all().order_by('-release_date')
    return render(request, 'movies/dashboard/dashboard.html', {'movies': movies})


def movie_detail(request, movie_id):
    movie = get_object_or_404(Movie, id=movie_id)
    return render(request, 'movies/dashboard/detail.html', {'movie': movie})




