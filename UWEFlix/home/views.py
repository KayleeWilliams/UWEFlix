from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from home.models import Film, Showing
import requests
import json

# Create your views here.
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
      'date': showing.date.strftime('%Y-%m-%d'),
      'time': showing.time.strftime('%H:%M'),
      'seats': showing.seats
  }


def makeExamples(): 
  Film.objects.all().delete()
  Showing.objects.all().delete()

  film = Film(title="The Owl House", description="The Owl House follows Luz, a self-assured teenage girl who accidentally stumbles upon a portal to a magical world where she befriends a rebellious witch, Eda, and an adorably tiny warrior, King.",
              duration=23, age_rating=9, imdb="tt8050756")
  film.save()

  # Create list of showings
  showings = [
      Showing(film=film, date='2022-01-01', time='20:00', seats=60, screen=1),
      Showing(film=film, date='2022-01-02', time='16:00', seats=80, screen=2),
      Showing(film=film, date='2022-01-02', time='18:00', seats=20, screen=1),
  ]

  Showing.objects.bulk_create(showings)

  film = Film(title="Strange World", description="The original action-adventure journeys deep into an uncharted and treacherous land where fantastical creatures await the legendary Clades, a family of explorers whose differences threaten to topple their latest - and by far - most crucial mission.",
              duration=102, age_rating=12, imdb="tt10298840")
  film.save()

  # Create list of showings
  showings = [
      Showing(film=film, date='2022-01-01', time='20:00', seats=100, screen=1),
      Showing(film=film, date='2022-01-01', time='21:00', seats=90, screen=2),
  ]

  Showing.objects.bulk_create(showings)
  