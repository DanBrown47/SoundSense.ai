from django.db import models
from django.contrib.auth.models import User
from django.core.validators import FileExtensionValidator
from . choices import genres, tags

class Song(models.Model):
    original_filename = models.CharField(max_length=300, blank=True, unique=True)
    title = models.CharField(max_length=150, blank=True, null=True)
    audio_file = models.FileField(max_length=350, upload_to='audio', validators=[FileExtensionValidator( ['m4a','mp3','wav'] )])
    artist = models.CharField(max_length=250, blank=True, null=True)
    album = models.CharField(max_length=250, blank=True, null=True)
    duration = models.DurationField(null=True, blank=True)
    released = models.DateField(null=True, blank=True)
    album_artist = models.CharField(max_length=250, blank=True, null=True)
    track_number = models.PositiveSmallIntegerField(blank=True, null=True, default=None)
    artwork = models.ImageField(max_length=350, upload_to='cover_images', default='cover_images/default.png', blank=True, null=True)
    lyrics = models.TextField(null=True, blank=True)
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
    
class Preference(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    metadata = models.FloatField()
    engagement = models.FloatField()
    instrument = models.FloatField()
    danceability = models.FloatField()
    acoustics = models.FloatField()
    aggressive = models.FloatField()
    happy = models.FloatField()
    party = models.FloatField()
    relaxed = models.FloatField()
    sad = models.FloatField()
    tonality = models.FloatField()
    reverb = models.FloatField()
    gender = models.FloatField()
    voice = models.FloatField()
    year = models.FloatField()

    def __str__(self):
        return "Preference of " + str(self.user.username)
    

