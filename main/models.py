from django.db import models
from django.core.validators import FileExtensionValidator
from ckeditor.fields import RichTextField
from django.db.models.signals import pre_save, pre_delete, post_save
from datetime import timedelta, datetime
import music_tag

class Song(models.Model):
    title = models.CharField(max_length=80, blank=True, null=True)
    audio_file = models.FileField(upload_to='audio', validators=[FileExtensionValidator( ['m4a','mp3','wav'] )])
    artist = models.CharField(max_length=80, blank=True, null=True)
    album = models.CharField(max_length=80, blank=True, null=True)
    duration = models.DurationField(null=True, blank=True)
    released = models.DateField(null=True, blank=True)
    album_artist = models.CharField(max_length=80, blank=True, null=True)
    track_number = models.PositiveSmallIntegerField(blank=True, null=True, default=None)
    artwork = models.ImageField(upload_to='cover_images', default='cover_images/default.jpg', blank=True, null=True)
    lyrics = RichTextField(blank=True, null=True)
    processed = models.BooleanField(default=False)

    def __str__(self):
        return str(self.title) + " - " + str(self.artist)
    
ALL_TAGS = (("ambient", "Ambient"),
            ("classical", "Classical"),
            ("electronic", "Electronic"),
            ("indie", "Indie"),
            ("metal", "Metal"),
            ("orchestral", "Orchestral"),
            ("pop", "Pop"),
            ("rock", "Rock"),
            ("funk", "Funk"),
            ("hiphop", "Hip-hop"),
            ("techno", "Techno"))

class Tags(models.Model):
    name = models.CharField(max_length=25, choices=ALL_TAGS, null=True, default=None, blank=True)
    song = models.ForeignKey(Song, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
    
def fill_database_with_metadata(sender, instance, created, *args, **kwargs):
    if created:
        file_field = instance.audio_file
        if file_field and file_field.file:
            audio_file = file_field.file
            try:
                audio = music_tag.load_file(str(audio_file))
                print("audio loaded")
                print(instance.artwork)
                instance.title = audio['tracktitle'] if instance.title  == None and 'tracktitle' in audio.tag_map.keys() else None
                instance.artist = audio['artist'] if instance.artist  == None and 'artist' in audio.tag_map.keys() else None
                instance.album = audio['album'] if instance.album  == None and 'album' in audio.tag_map.keys() else None
                instance.album_artist = audio['albumartist'] if instance.album_artist  == None and 'albumartist' in audio.tag_map.keys() else None
                instance.track_number = audio['tracknumber'] if instance.track_number  == None and 'tracknumber' in audio.tag_map.keys() else None
                instance.lyrics = str(audio['lyrics']) if instance.lyrics  == None and 'lyrics' in audio.tag_map.keys() else None
                instance.duration = timedelta(seconds=int(audio['#length'])) if instance.duration  == None and '#length' in audio.tag_map.keys() else None
                #instance.released = datetime(year=int(audio['year'])) if instance.released  == None and 'year' in audio.tag_map.keys() else None
                #instance.artwork = audio['artwork'].first.thumbnail([500, 500]) if instance.artwork  == 'cover_images/default.jpg' and 'artwork' in audio.tag_map.keys() else None
                instance.artwork.save('image.jpg', audio['artwork'].first.thumbnail([500, 500]), save=True)
                print(instance.artwork)
                instance.save()
            except:
                print("Unsupported format")

            #print(audio, type(audio))


post_save.connect(fill_database_with_metadata, Song)
