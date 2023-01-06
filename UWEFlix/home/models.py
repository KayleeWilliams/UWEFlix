from django.db import models

# Create your models here.
class Film(models.Model):
    title = models.CharField(max_length=255)
    imdb = models.TextField()
    description = models.TextField()
    duration = models.PositiveIntegerField()
    age_rating = models.PositiveIntegerField()
    image_url = models.URLField(blank=True, null=True)
    backdrop_url = models.URLField(blank=True, null=True)


# Cascade (On film deletion, delete all related showings)
class Showing(models.Model):
    film = models.ForeignKey(Film, on_delete=models.CASCADE, related_name='showings')
    date = models.DateField()
    time = models.TimeField()
    seats = models.PositiveIntegerField() # Initiized by screen total seats
    screen = models.PositiveIntegerField() # Forign key to screen model (not yet created)
class Ticket(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=6, decimal_places=2)

# Store ticket type and quantity
class TicketTypeQuantity(models.Model):
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
class Booking(models.Model):
    showing = models.ForeignKey(Showing, on_delete=models.CASCADE)
    customer_name = models.CharField(max_length=100)
    customer_email = models.EmailField()
    ticket_type_quantities = models.ManyToManyField(TicketTypeQuantity) # User can select multiple ticket types and quantities
