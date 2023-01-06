from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template import loader
from home.models import Film, Showing, Ticket, Booking, TicketTypeQuantity
from home.forms import BookingForm
import requests
import json

# Create your views here.
def booking(request):
  if 'showing' not in request.GET:
    return redirect('/')

  # Get showing
  showing_id = request.GET['showing']
  showing = Showing.objects.get(id=showing_id)

  # Form submission
  if request.method == 'POST':
    form = BookingForm(request.POST, available_tickets=Ticket.objects.all())

    if form.is_valid():
      # Further validation 
      # Check if there are enough seats + Seats > 0
      total_tickets = 0
      for field_name, quantity in form.cleaned_data.items():
          if field_name.startswith('ticket_'):
              total_tickets += quantity

      if total_tickets > showing.seats:
          form.add_error(None, 'Not enough seats available.')
          return render(request, 'booking.html', {'form': form, 'showing': showing})

      elif total_tickets == 0:
          form.add_error(None, 'You must select at least one ticket.')
          return render(request, 'booking.html', {'form': form, 'showing': showing})

      booking = Booking.objects.create(
          showing=showing,
          customer_name=form.cleaned_data['customer_name'],
          customer_email=form.cleaned_data['customer_email'],
      )
      
      # Create ticket type quantities for each ticket type the user booked
      for field_name, quantity in form.cleaned_data.items():
          if field_name.startswith('ticket_'):
              ticket_id = field_name.split('_')[1]
              ticket = Ticket.objects.get(id=ticket_id)
              ttq = TicketTypeQuantity.objects.create(ticket=ticket, quantity=quantity)
              booking.ticket_type_quantities.add(ttq)

      # Update showing seats & save booking
      showing.seats -= total_tickets
      showing.save()
      booking.save()
      return render(request, 'booking-confirmation.html', {'booking': booking})
    else:
        form = BookingForm(available_tickets=Ticket.objects.all())
    return render(request, 'booking.html', {'form': form, 'showing': showing})
  
  else: 
    form = BookingForm(available_tickets=Ticket.objects.all())
    return render(request, 'booking.html', {'form': form, 'showing': showing})


def home(request):
  template = loader.get_template('home.html')

  # MAKE TEMP DATA
  makeExamples()

  films = Film.objects.all().prefetch_related('showings')
  
  # Get film posters by IMDB ID using an API
  for film in films:
    response = requests.get(f'https://api.themoviedb.org/3/find/{film.imdb}?api_key=d4c4c2d25e196ead918fc7080850a0d7&language=en-US&external_source=imdb_id')
    data = response.json()
    for category in data.keys():
      if len(data[category]) > 0:
        film.image_url = f"https://image.tmdb.org/t/p/original{data[category][0]['poster_path']}"
        film.backdrop_url = f"https://image.tmdb.org/t/p/original{data[category][0]['backdrop_path']}"
        film.save()

    # Serialize films
    serialized_films = [film_serializable(film) for film in films]
    context = {
        'films': serialized_films,
    }

  return render(request, 'home.html', context)


def film_serializable(film):
  # Serialize the showings
  serialized_showings = [showing_serializable(showing) for showing in film.showings.all()]

  return {
    'title': film.title,
    'description': film.description,
    'duration': film.duration,
    'age_rating': film.age_rating,
    'image_url': film.image_url,
    'showings': serialized_showings,
  }


def showing_serializable(showing):
  return {
    'id': showing.id,
    'date': showing.date.strftime('%Y-%m-%d'),
    'time': showing.time.strftime('%H:%M'),
    'seats': showing.seats
  }


def makeExamples(): 
  # Delete all data before making new
  Film.objects.all().delete()
  Showing.objects.all().delete()
  Ticket.objects.all().delete()
  Booking.objects.all().delete()

  # Create tickets
  tickets = [
      Ticket(name="Adult", price=7.50),
      Ticket(name="Child", price=3.00),
      Ticket(name="Student", price=5.00),
  ]

  Ticket.objects.bulk_create(tickets)

  # Create film + showings
  film = Film(title="The Owl House", description="The Owl House follows Luz, a self-assured teenage girl who accidentally stumbles upon a portal to a magical world where she befriends a rebellious witch, Eda, and an adorably tiny warrior, King.",
              duration=23, age_rating=9, imdb="tt8050756")
  film.save()

  # Create list of showings
  showings = [
      Showing(film=film, date='2023-01-01', time='20:00', seats=60, screen=1),
      Showing(film=film, date='2023-01-02', time='16:00', seats=80, screen=2),
      Showing(film=film, date='2023-01-02', time='18:00', seats=20, screen=1),
  ]

  Showing.objects.bulk_create(showings)

  film = Film(title="Strange World", description="The original action-adventure journeys deep into an uncharted and treacherous land where fantastical creatures await the legendary Clades, a family of explorers whose differences threaten to topple their latest - and by far - most crucial mission.",
              duration=102, age_rating=12, imdb="tt10298840")
  film.save()

  # Create list of showings
  showings = [
      Showing(film=film, date='2023-01-01', time='20:00', seats=100, screen=1),
      Showing(film=film, date='2023-01-01', time='21:00', seats=90, screen=2),
  ]

  Showing.objects.bulk_create(showings)
  
  film = Film(title="Glass Onion: A Knives Out Mystery", description="Tech billionaire Miles Bron invites his friends for a getaway on his private Greek island. When someone turns up dead, Detective Benoit Blanc is put on the case.",
              duration=139, age_rating=12, imdb="tt11564570")
  film.save()

  showings = [
      Showing(film=film, date='2023-01-05', time='09:00', seats=100, screen=1),
      Showing(film=film, date='2023-01-05', time='12:00', seats=100, screen=1),
  ]
  Showing.objects.bulk_create(showings)

  film = Film(title="John Wick: Chapter 4", description="John Wick uncovers a path to defeating The High Table. But before he can earn his freedom, Wick must face off against a new enemy with powerful alliances across the globe and forces that turn old friends into foes.",
              duration=200, age_rating=14, imdb="tt10366206")
  film.save()

  showings = [
      Showing(film=film, date='2023-01-05', time='10:00', seats=50, screen=3),
  ]
  Showing.objects.bulk_create(showings)

  film = Film(title="Top Gun: Maverick", description="After thirty years, Maverick is still pushing the envelope as a top naval aviator, but must confront ghosts of his past when he leads TOP GUN's elite graduates on a mission that demands the ultimate sacrifice from those chosen to fly it.",
              duration=130, age_rating=12, imdb="tt1745960")
  film.save()

  showings = [
      Showing(film=film, date='2023-01-05', time='16:00', seats=20, screen=20),
      Showing(film=film, date='2023-01-06', time='16:00', seats=20, screen=20),
      Showing(film=film, date='2023-01-07', time='16:00', seats=50, screen=20),


  ]
  Showing.objects.bulk_create(showings)

  film = Film(title="The Batman", description="When a sadistic serial killer begins murdering key political figures in Gotham, Batman is forced to investigate the city's hidden corruption and question his family's involvement.",
              duration=176, age_rating=15, imdb="tt1877830")
  film.save()

  showings = [
      Showing(film=film, date='2023-01-06', time='20:00', seats=60, screen=1),
      Showing(film=film, date='2023-01-07', time='16:00', seats=80, screen=2),
      Showing(film=film, date='2023-01-07', time='18:00', seats=20, screen=1),


  ]
  Showing.objects.bulk_create(showings)

  film = Film(title="Arcane", description="Set in utopian Piltover and the oppressed underground of Zaun, the story follows the origins of two iconic League champions-and the power that will tear them apart.",
              duration=360, age_rating=15, imdb="tt11126994")
  film.save()

  showings = [
      Showing(film=film, date='2023-01-12', time='20:00', seats=60, screen=1),
      Showing(film=film, date='2023-01-12', time='16:00', seats=80, screen=2),
  ]
  Showing.objects.bulk_create(showings)

  film = Film(title="Wednesday", description="Follows Wednesday Addams' years as a student, when she attempts to master her emerging psychic ability, thwart and solve the mystery that embroiled her parents.",
              duration=360, age_rating=12, imdb="tt13443470")
  film.save()

  showings = [
      Showing(film=film, date='2023-01-13', time='10:00', seats=60, screen=1),
      Showing(film=film, date='2023-01-13', time='14:00', seats=80, screen=2),
  ]
  Showing.objects.bulk_create(showings)
