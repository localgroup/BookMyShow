from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Review
from movies.models import Movie
from accounts.models import User
from django.contrib import messages


# Create your views here.


@login_required
def add_review(request, slug):
    movie = get_object_or_404(Movie, slug=slug)
    user = request.user
    if request.method == 'POST':
        # Note: The template uses 'value' for the rating input, not 'rating'
        rating = request.POST.get('value')
        comment = request.POST.get('comment')

        if rating is not None and rating != '':
            review = Review.objects.create(
                user=user,
                movie=movie,
                rating=int(rating),
                comment=comment
            )
            messages.success(request, 'Review added successfully!')
            return redirect('movie_detail', slug=movie.slug)
        else:
            messages.error(request, 'Rating is required.')
    
    # You may want to pass 'rating_range' to the template for the rating form
    rating_range = range(1, 11)
    return render(request, 'dashboard/movie_detail.html', {'movie': movie, 'rating_range': rating_range})