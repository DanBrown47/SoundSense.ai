from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver
from django.contrib.auth.models import User
from datetime import timedelta, datetime
from . models import Song, Preference
import music_tag
import regex as re
from .choices import balancing_factor, instrument_weightage, feature_weights

@receiver(post_save, sender=Song)
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
                    instance.lyrics = re.sub(r'\[.*?\]', '', str(audio['lyrics']).replace('\n', '<br>'))
                
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

@receiver(pre_delete, sender=Song)
def delete_files(sender, instance, *args, **kwargs):
    instance.audio_file.delete(False)
    if instance.artwork.name != 'cover_images/default.png':
        instance.artwork.delete(False)

@receiver(post_save, sender=User)
def create_default_preferences(sender, instance, created, *args, **kwargs):
    if created:
        if not Preference.objects.filter(user=instance).exists():
            pref = Preference()
            pref.user = instance
            pref.metadata = balancing_factor
            pref.instrument = instrument_weightage
            pref.engagement = feature_weights['Engagement']
            pref.danceability = feature_weights['danceability']
            pref.acoustics = feature_weights['mood_acoustic']
            pref.aggressive = feature_weights['mood_aggressive']
            pref.happy = feature_weights['mood_happy']
            pref.party = feature_weights['mood_party']
            pref.relaxed = feature_weights['mood_relaxed']
            pref.sad = feature_weights['mood_sad']
            pref.tonality = feature_weights['tonal']
            pref.reverb = feature_weights['Reverb_wet']
            pref.gender = feature_weights['voice_female']
            pref.voice = feature_weights['overall_voice']
            pref.year = feature_weights['year']
            pref.tonality = feature_weights['tonal']
            pref.save()
