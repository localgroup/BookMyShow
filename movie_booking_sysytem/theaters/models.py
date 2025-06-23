from django.db import models

# Create your models here.

class Theater(models.Model):
    name = models.CharField(max_length=200)
    city = models.CharField(max_length=255)
    address = models.CharField()
    
    
seat_type_choices = [
    ['silver', 'Silver'],
    ['gold', 'Gold'],
    ['recliner', 'Recliner']
    ]

seat_level_choices = [
    ['ground', 'Ground'],
    ['first', 'First'],
    ['second', 'Second']
]


class Seat(models.Model):
    theater = models.ForeignKey(Theater, on_delete=models.CASCADE)
    seat_number = models.IntegerField()
    row_level = models.CharField(max_length=100, choices=seat_level_choices)
    seat_type = models.CharField(max_length=100, choices=seat_type_choices)
    is_booked = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.seat_number} - {self.seat_type})"