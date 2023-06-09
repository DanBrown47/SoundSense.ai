from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Case, When
from django.core.paginator import Paginator
from django.core.files.storage import FileSystemStorage
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.contrib.auth import authenticate, login
from django.contrib.admin.views.decorators import staff_member_required
from . models import Song
from .forms import SongForm, UserRegistrationForm, UserPreferenceForm, SongUploadForm, LoginForm
from .utils import get_similar_songs_id, train_model, update_songs_in_database_to_csv, update_csv_files_upon_model_deletion, fill_genres_and_tags, extract_metadata, upload_and_check_similarity
import os

class ReplaceExistingStorage(FileSystemStorage):
    def get_available_name(self, name, max_length=None):
        # Delete the existing file if it already exists
        if self.exists(name):
            self.delete(name)
        return name
    
def home(request):
    return render(request, 'home.html')

def All_songs(request):
    all_songs = Song.objects.all().order_by('title')
    paginator = Paginator(all_songs, 48)  # Show 10 products per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'all_songs.html', {'page_obj': page_obj})

def Search_song(request):
    title = request.GET['title'] if ('title' in request.GET) else None
    artist = request.GET['artist'] if ('artist' in request.GET) else None
    
    if title and title != "" and artist and artist != "":
        all_songs = Song.objects.filter(title__icontains=title, artist__icontains=artist)
    elif artist and artist != "":
        all_songs = Song.objects.filter(artist__icontains=artist)
    elif title and title != "":
        all_songs = Song.objects.filter(title__icontains=title)
    else:
        all_songs = None

    context = {
        'song_results': all_songs
    }
    return render(request, 'search.html', context)

def song(request, song_id):
    current_song = get_object_or_404(Song, id=song_id)    
    similar_songs_id = get_similar_songs_id(request, song_id)[:8]
    order_expression = Case(*[When(id=id_val, then=pos) for pos, id_val in enumerate(similar_songs_id)],default=len(similar_songs_id))
    matching_models = Song.objects.filter(id__in=similar_songs_id).order_by(order_expression)
    
    context = {
        'current_song': current_song,
        'similar_songs': matching_models
    }
    return render(request, 'song.html', context)

def is_superuser(user):
    return user.is_superuser

@staff_member_required(login_url='login')
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
    return render(request, 'upload_music.html', {'form': songform})

def Register(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Registered successfully")
            return redirect('home')
    else:
        form = UserRegistrationForm()
    return render(request, 'register.html', {'form': form})

def Login(request):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('dashboard')
    else:
        form = LoginForm(request)
    
    return render(request, 'login.html', {'form': form})

def Logout(request):
    logout(request)
    return redirect('login')

@login_required(login_url='login')       
def Search_individual(request):
    if 'search_results' in request.session:
        similar_songs_id = request.session.get('search_results', [])[:8]
        order_expression = Case(*[When(id=id_val, then=pos) for pos, id_val in enumerate(similar_songs_id)],default=len(similar_songs_id))
        matching_models = Song.objects.filter(id__in=similar_songs_id).order_by(order_expression)
        
    context = {
        'similar_songs': matching_models
    }
    return render(request, 'search_individual.html', context)

@login_required(login_url='login')
def Dashboard(request):
    form_pref = UserPreferenceForm(instance=request.user.preference)
    form_song = SongUploadForm()

    if request.method == 'POST':
        if 'form_song' in request.POST and request.FILES.get('file'):
            form_song = SongUploadForm(request.POST, request.FILES)
            if form_song.is_valid():
                song_file = request.FILES['file']
                fss = ReplaceExistingStorage(location='media/uploads/')
                file_extension = os.path.splitext(song_file.name)[1]
                new_filename = 'temp_' + str(request.user.username) + file_extension
                # Save the uploaded file to the specified location
                file = fss.save(new_filename, song_file)
                file_url = 'uploads/' + str(file)
                request.session['search_results'] = upload_and_check_similarity(request, file_path=file_url)
                return redirect('search_individual')
        elif 'form_pref' in request.POST:
            form_pref = UserPreferenceForm(request.POST, instance=request.user.preference)
            if form_pref.is_valid():
                form_pref.save()
                return redirect('dashboard')
            
    context = {
        'form_pref': form_pref,
        'form_song': form_song
    }
    return render(request,'userdash.html', context)

@staff_member_required(login_url='login')
def update_csv_files(request):
    update_songs_in_database_to_csv()
    extract_metadata()
    update_csv_files_upon_model_deletion()
    return redirect(request.META['HTTP_REFERER'])

@staff_member_required(login_url='login')
def retrain_model(request):
    train_model()
    return redirect(request.META['HTTP_REFERER'])

@staff_member_required(login_url='login')
def update_genre_tags_processed(request):
    fill_genres_and_tags()
    return redirect(request.META['HTTP_REFERER'])

