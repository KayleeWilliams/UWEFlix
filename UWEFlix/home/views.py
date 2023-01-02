from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from home.models import Film, Showing

# Create your views here.
def home(request):
  template = loader.get_template('home.html')

  # MAKE TEMP DATA
  makeExamples()

  films = Film.objects.all().prefetch_related('showings')
  return render(request, 'home.html', {'films': films})

def makeExamples(): 
  Film.objects.all().delete()
  Showing.objects.all().delete()

  film = Film(title="The Owl House", description="The Owl House follows Luz, a self-assured teenage girl who accidentally stumbles upon a portal to a magical world where she befriends a rebellious witch, Eda, and an adorably tiny warrior, King.",
              duration=23, age_rating=9)
  film.save()

  # Create list of showings
  showings = [
      Showing(film=film, date='2022-01-01', time='20:00', seats=60, screen=1),
      Showing(film=film, date='2022-01-02', time='16:00', seats=80, screen=2),
      Showing(film=film, date='2022-01-02', time='18:00', seats=20, screen=1),
  ]

  film = Film(title="Strange World", description="TThe original action-adventure journeys deep into an uncharted and treacherous land where fantastical creatures await the legendary Clades, a family of explorers whose differences threaten to topple their latest - and by far - most crucial mission.",
              duration=102, age_rating=12)
  film.save()

  # Create list of showings
  showings = [
      Showing(film=film, date='2022-01-01', time='20:00', seats=100, screen=1),
      Showing(film=film, date='2022-01-01', time='21:00', seats=90, screen=2),
  ]

  Showing.objects.bulk_create(showings)
  