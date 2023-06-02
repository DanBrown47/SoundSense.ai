from django.contrib import admin
from .models import Song, Tag, Genre

class Song_Tags_Admin(admin.TabularInline):
    model = Tag

class Song_Genre_Admin(admin.TabularInline):
    model = Genre

class Song_Admin(admin.ModelAdmin):
    inlines = (Song_Genre_Admin, Song_Tags_Admin)
    list_display = ('title', 'artist', 'album','album_artist','released','processed')
    
    def save_model(self, request, obj, form, change):
        if request.FILES.get('audio_file'):
            original_filename = request.FILES['audio_file'].name
            real_name = ".".join(original_filename.split('.')[:-1])
            obj.original_filename = real_name
        # Save the model
        super().save_model(request, obj, form, change)

admin.site.register(Song, Song_Admin)