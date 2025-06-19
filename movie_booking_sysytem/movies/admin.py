from django.contrib import admin
from . import models

# Register your models here.

@admin.register(models.Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ('title', 'genre', 'language', 'release_date', 'status', 
                    'created_at', 'movie_image', 'trailer_url', 'synopsis', 
                    'duration_minutes', )
    
    
@admin.register(models.Cast)
class CastAdmin(admin.ModelAdmin):
    list_display = ('movie', 'name', 'role', 'image')