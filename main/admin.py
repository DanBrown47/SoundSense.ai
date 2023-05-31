from django.contrib import admin
from .models import Song, Tags

class Song_Tags_Admin(admin.TabularInline):
    model = Tags
class Song_Admin(admin.ModelAdmin):
    inlines = (Song_Tags_Admin,)
    list_display = ('title', 'artist', 'album','album_artist','released','processed')
    
admin.site.register(Song, Song_Admin)
admin.site.register(Tags)