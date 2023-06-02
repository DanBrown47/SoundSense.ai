from django.db import models
from django.core.validators import FileExtensionValidator
from ckeditor.fields import RichTextField
from django.db.models.signals import pre_delete, post_save
from datetime import timedelta, datetime
import music_tag
from .choices import tags, genres

class Song(models.Model):
    original_filename = models.CharField(max_length=300, blank=True)
    title = models.CharField(max_length=150, blank=True, null=True)
    audio_file = models.FileField(max_length=350, upload_to='audio', validators=[FileExtensionValidator( ['m4a','mp3','wav'] )])
    artist = models.CharField(max_length=250, blank=True, null=True)
    album = models.CharField(max_length=250, blank=True, null=True)
    duration = models.DurationField(null=True, blank=True)
    released = models.DateField(null=True, blank=True)
    album_artist = models.CharField(max_length=250, blank=True, null=True)
    track_number = models.PositiveSmallIntegerField(blank=True, null=True, default=None)
    artwork = models.ImageField(max_length=350, upload_to='cover_images', default='cover_images/default.png', blank=True, null=True)
    lyrics = RichTextField(blank=True, null=True)
    processed = models.BooleanField(default=False)

    def __str__(self):
        if self.title == None or self.artist == None:
            return self.original_filename
        else:
            return str(self.title) + " - " + str(self.artist)

class Genre(models.Model):
    name = models.CharField(max_length=35, choices=genres, null=True, default=None, blank=True)
    song = models.ForeignKey(Song, on_delete=models.CASCADE)
    score = models.DecimalField(max_digits=8, decimal_places=4, blank=True, null=True)

    def __str__(self):
        return self.name

class Tag(models.Model):
    name = models.CharField(max_length=35, choices=tags, null=True, default=None, blank=True)
    song = models.ForeignKey(Song, on_delete=models.CASCADE)
    score = models.DecimalField(max_digits=8, decimal_places=4, blank=True, null=True)
    
    def __str__(self):
        return self.name
    
def fill_database_with_metadata(sender, instance, created, *args, **kwargs):
    if created:
        file_field = instance.audio_file
        if file_field and file_field.file:
            audio_file = str(file_field.file)
            file_name = ".".join(audio_file.split('media/audio/')[1].split('.')[:-1])
            try:
                audio = music_tag.load_file(audio_file)
                #print("audio loaded")
                instance.title = audio['tracktitle'] if instance.title == None and 'tracktitle' in audio.tag_map.keys() else instance.title
                instance.artist = audio['artist'] if instance.artist == None and 'artist' in audio.tag_map.keys() else instance.artist
                instance.album = audio['album'] if instance.album == None and 'album' in audio.tag_map.keys() else instance.album
                instance.album_artist = audio['albumartist'] if instance.album_artist == None and 'albumartist' in audio.tag_map.keys() else instance.album_artist
                instance.track_number = audio['tracknumber'] if instance.track_number == None and 'tracknumber' in audio.tag_map.keys() else instance.track_number

                if instance.lyrics == None and 'lyrics' in audio.tag_map.keys():
                    instance.lyrics = audio['lyrics'] 
                instance.duration = timedelta(seconds=int(audio['#length'])) if instance.duration == None and '#length' in audio.tag_map.keys() else instance.duration

                if (instance.released == None) and ('year' in audio.tag_map.keys()) and str(audio['year']) != "":
                    instance.released = datetime(year=int(audio['year']),month=1, day=1)

                if instance.artwork == 'cover_images/default.png' and 'artwork' in audio.tag_map.keys():
                    try:
                        pil_image = audio['artwork'].first.thumbnail([500, 500])
                        image_file = "media/cover_images/" + file_name + ".jpg"
                        pil_image.save(image_file)
                        instance.artwork = "cover_images/" + file_name + ".jpg"
                    except:
                        pass
                instance.save()
            except:
                print("Unsupported format")

            #print(audio, type(audio))


post_save.connect(fill_database_with_metadata, Song)

def delete_files(sender, instance, *args, **kwargs):
    instance.audio_file.delete(False)
    if instance.artwork.name != 'cover_images/default.png':
        instance.artwork.delete(False)

pre_delete.connect(delete_files, Song)

