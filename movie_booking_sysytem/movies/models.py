from django.db import models
from django.utils.text import slugify
from django.db.models import UniqueConstraint

# Create your models here.

genres = [
    ('Action', 'Action'),
    ('Adventure', 'Adventure'),
    ('Comedy', 'Comedy'),
    ('Drama', 'Drama'),
    ('Fantasy', 'Fantasy'),
    ('Horror', 'Horror'),
    ('Mystery', 'Mystery'),
    ('Romance', 'Romance'),
    ('Sci-Fi', 'Sci-Fi'),
    ('Thriller', 'Thriller'),
    ('Western', 'Western'),
]

languages = [
    ('English', 'English'),
    ('Hindi', 'Hindi'),
    ('Tamil', 'Tamil'),
    ('Telugu', 'Telugu'),
    ('Kannada', 'Kannada'),
    ('Malayalam', 'Malayalam'),
    ('Bengali', 'Bengali'),
]

class Movie(models.Model):
    title = models.CharField(max_length=100)
    genre = models.CharField(max_length=255, choices=genres, null=True, blank=True)
    language = models.CharField(max_length=255, choices=languages, null=True, blank=True)
    synopsis = models.TextField(null=True, blank=True)
    duration_minutes = models.PositiveIntegerField(null=True, blank=True)
    release_date = models.DateField(null=True, blank=True)
    trailer_url = models.URLField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=[('Upcoming', 'Upcoming'), ('Released', 'Released')], null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    movie_image = models.URLField(null=True, blank=True)
    slug = models.SlugField(max_length=100, unique=True, null=True, blank=True)

    
    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)
    
    
class Cast(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='casts')
    name = models.CharField(max_length=255)
    role = models.CharField(max_length=255, null=True, blank=True)
    image = models.ImageField(upload_to='casts/', null=True, blank=True)
