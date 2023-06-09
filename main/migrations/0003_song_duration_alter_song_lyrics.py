# Generated by Django 4.2.1 on 2023-05-30 10:13

import ckeditor.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_alter_song_lyrics_alter_song_track_number'),
    ]

    operations = [
        migrations.AddField(
            model_name='song',
            name='duration',
            field=models.DurationField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='song',
            name='lyrics',
            field=ckeditor.fields.RichTextField(blank=True, null=True),
        ),
    ]
