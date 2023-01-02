from django.db import models

# Create your models here.
class Film(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    duration = models.PositiveIntegerField()
    age_rating = models.PositiveIntegerField()

# Cascade (On film deletion, delete all related showings)
class Showing(models.Model):
    film = models.ForeignKey(Film, on_delete=models.CASCADE, related_name='showings')
    date = models.DateField()
    time = models.TimeField()
    seats = models.PositiveIntegerField() # Initiized by screen total seats
    screen = models.PositiveIntegerField() # Forign key to screen model (not yet created)

class Booking(models.Model):
    showing = models.ForeignKey(Showing, on_delete=models.CASCADE)
    customer_name = models.CharField(max_length=100)
    customer_email = models.EmailField()
    seats = models.PositiveIntegerField()
