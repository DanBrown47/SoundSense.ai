# Generated by Django 4.2.1 on 2023-06-01 04:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0010_delete_song_id'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Tags',
            new_name='Tag',
        ),
    ]
