from django.shortcuts import render
from django.core.files import File
import music_tag
from . models import Song

# Create your views here.
def home(request):
    songs = Song.objects.all()
    context = {
        'songs': songs
    }
    return render(request, 'home.html', context)