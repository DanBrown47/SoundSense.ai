from django.shortcuts import render
from . models import Song
from .forms import SongForm

def home(request):
    songs = Song.objects.all()
    context = {
        'songs': songs
    }
    return render(request, 'home.html', context)

def song(request):
    songs = Song.objects.all()
    song = songs.first()
    context = {
        'songs': songs
    }
    print(song.audio_file.name)
    return render(request, 'song.html', context)

def upload_music(request):
    if request.method == "POST":
        songform = SongForm(request.POST, request.FILES) 
        if songform.is_valid():
            files = songform.cleaned_data["file"]
            for file in files:
                real_name = ".".join(str(file).split('.')[:-1])
                Song.objects.create(audio_file=file, original_filename=real_name)
    else:
        songform = SongForm()  
    return render(request, 'upload_music.html', {'form':songform})