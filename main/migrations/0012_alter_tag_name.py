# Generated by Django 4.2.1 on 2023-06-02 13:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0011_rename_tags_tag'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tag',
            name='name',
            field=models.CharField(blank=True, choices=[('Tag_ambient', 'Ambient'), ('Tag_atmospheric', 'Atmospheric'), ('Tag_chillout', 'Chillout'), ('Tag_classical', 'Classical'), ('Tag_downtempo', 'Downtempo'), ('Tag_easylistening', 'Easylistening'), ('Tag_electronic', 'Electronic'), ('Tag_folk', 'Folk'), ('Tag_funk', 'Funk'), ('Tag_hiphop', 'Hiphop'), ('Tag_house', 'House'), ('Tag_indie', 'Indie'), ('Tag_instrumentalpop', 'Instrumentalpop'), ('Tag_jazz', 'Jazz'), ('Tag_metal', 'Metal'), ('Tag_newage', 'Newage'), ('Tag_orchestral', 'Orchestral'), ('Tag_pop', 'Pop'), ('Tag_popfolk', 'Popfolk'), ('Tag_poprock', 'Poprock'), ('Tag_reggae', 'Reggae'), ('Tag_rock', 'Rock'), ('Tag_techno', 'Techno'), ('Tag_triphop', 'Triphop'), ('Tag_acousticguitar', 'Acousticguitar'), ('Tag_bass', 'Bass'), ('Tag_drummachine', 'Drummachine'), ('Tag_drums', 'Drums'), ('Tag_electricguitar', 'Electricguitar'), ('Tag_electricpiano', 'Electricpiano'), ('Tag_guitar', 'Guitar'), ('Tag_keyboard', 'Keyboard'), ('Tag_piano', 'Piano'), ('Tag_strings', 'Strings'), ('Tag_synthesizer', 'Synthesizer'), ('Tag_violin', 'Violin'), ('Tag_emotional', 'Emotional'), ('Tag_film', 'Film'), ('Tag_relaxing', 'Relaxing')], default=None, max_length=25, null=True),
        ),
    ]
