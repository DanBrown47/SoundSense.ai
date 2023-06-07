from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Case, When
from . models import Song
from .forms import SongForm
from .utils import get_similar_songs_id, train_model, update_songs_in_database_to_csv, update_csv_files_upon_model_deletion, fill_genres_and_tags, extract_metadata

def home(request):
    songs = Song.objects.all()
    context = {
        'songs': songs
    }
    return render(request, 'home.html', context)

def song(request, song_id):
    current_song = get_object_or_404(Song, id=song_id)    
    similar_songs_id = get_similar_songs_id(song_id)[:8]
    order_expression = Case(*[When(id=id_val, then=pos) for pos, id_val in enumerate(similar_songs_id)],default=len(similar_songs_id))
    matching_models = Song.objects.filter(id__in=similar_songs_id).order_by(order_expression)
    
    context = {
        'current_song': current_song,
        'similar_songs': matching_models
    }
    return render(request, 'song.html', context)

def update_csv_files(request):
    update_songs_in_database_to_csv()
    extract_metadata()
    update_csv_files_upon_model_deletion()
    return redirect(request.META['HTTP_REFERER'])

def retrain_model(request):
    train_model()
    return redirect(request.META['HTTP_REFERER'])

def update_genre_tags_processed(request):
    fill_genres_and_tags()
    return redirect(request.META['HTTP_REFERER'])

def upload_music(request):
    if request.method == "POST":
        songform = SongForm(request.POST, request.FILES) 
        if songform.is_valid():
            files = songform.cleaned_data["file"]
            for file in files:
                real_name = ".".join(str(file).split('.')[:-1])
                Song.objects.create(audio_file=file, original_filename=real_name)
            update_songs_in_database_to_csv()
    else:
        songform = SongForm()  
    return render(request, 'upload_music.html', {'form':songform})
