from essentia.standard import MonoLoader, TensorflowPredictEffnetDiscogs, TensorflowPredict2D
from data.OpenL3_embeddings import EmbeddingsOpenL3
import pandas as pd
import numpy as np
import json

df_django = pd.read_csv('data/songs_db.csv')
df_features = pd.read_csv('data/song_dataset_final.csv')

processed_songs = pd.read_csv('data/processed_songs.csv')
df_to_extract = df_django[~df_django['song name'].isin(processed_songs['song name'])]
audio_file_list = df_to_extract['file_path']

with open('data/weights_metadata.json') as json_file:
    model_weights_metadata = json.load(json_file)
json_file.close()
path = "data/all_classifiers_and_metadata/"
song_path = 'media/'
embedding_model_weights_l3 = "data/all_classifiers_and_metadata/openl3-music-mel128-emb512-3.pb"
embedding_model_weights_dsg = "data/all_classifiers_and_metadata/discogs-effnet-bs64-1.pb"

def extract_all_features(all_songs):
    column_labels = ['song name']
    rows = []
    flag = True

    for song in all_songs:
        extractor = EmbeddingsOpenL3(embedding_model_weights_l3)
        embeddings_l3 = extractor.compute(song_path + song)

        audio = MonoLoader(filename=song_path+song, sampleRate=44100, resampleQuality=4)()
        embedding_model = TensorflowPredictEffnetDiscogs(graphFilename=embedding_model_weights_dsg, output="PartitionedCall:1")
        embeddings_dsg = embedding_model(audio)

        classification_models = {}
        for key in model_weights_metadata:
            model_type = model_weights_metadata[key][0]
            file_name = model_weights_metadata[key][1]

            weight_file = path + file_name + ".pb"
            mdata_file = path + file_name + ".json"

            metadata = json.load(open(mdata_file, 'r'))
            input_ = metadata['schema']['inputs'][0]['name']
            output = metadata['schema']['outputs'][0]['name']
            classes = metadata['classes']

            model = TensorflowPredict2D(graphFilename=weight_file, output=output, input=input_)
            
            classification_models[key] = [model, model_type, classes]
            
        scores = [df_to_extract[df_to_extract['file_path'] == song]['song name'].values[0]]

        for key in classification_models:
            model = classification_models[key][0]
            model_type = classification_models[key][1]
            classes = classification_models[key][2]

            if model_type == "openl3":
                predictions = np.mean(model(embeddings_l3), axis=0)
            else:
                predictions = np.mean(model(embeddings_dsg), axis=0)

            if flag:
                for i in range(0, len(predictions)):
                    label = str(key) + "_" + str(classes[i])
                    column_labels.append(label)
        
            for i in range(0, len(predictions)):
                scores.append(predictions[i])
                
        flag = False
        rows.append(scores)
    return column_labels, rows

genre_to_drop = [  'Genre_experimental', 'Genre_alternative', 'Genre_soundtrack',  'Genre_newage', 'Genre_psychedelic', 'Genre_world', 'Genre_singersongwriter', 
'Genre_minimal', 'Genre_progressive', 'Genre_contemporary', 'Genre_grunge', 'Genre_rnb', 'Genre_dance', 'Genre_idm', 'Genre_90s', 'Genre_soul', 'Genre_chanson', 
'Genre_60s', 'Genre_newwave', 'Genre_worldfusion', 'Genre_celtic', 'Genre_alternativerock', 'Genre_electronica', 'Genre_improvisation', 'Genre_80s', 
'Genre_edm', 'Genre_latin', 'Genre_hard','Genre_70s', 'Genre_swing', 'Genre_bossanova', 'Genre_eurodance']

tags_to_drop = [  'Tag_energetic', 'Tag_trance', 'Tag_dance',  'Tag_happy', 'Tag_experimental', 'Tag_soundtrack', 'Tag_alternative', 
'Tag_world', 'Tag_lounge', 'Tag_voice', 'Tag_computer']

instruments_to_drop = ['Instrument_bell', 'Instrument_bongo', 'Instrument_clarinet', 'Instrument_pad', 'Instrument_voice',
        'Instrument_oboe', 'Instrument_rhodes',  'Instrument_computer',
        'Instrument_horn', 'Instrument_viola', 'Instrument_sampler']

other_columns_to_drop = ['danceability_not_danceable', 'mood_acoustic_non_acoustic', 'mood_aggressive_not_aggressive', 'mood_electronic_non_electronic', 
                         'mood_happy_non_happy', 'mood_party_non_party', 'mood_relaxed_non_relaxed', 'mood_sad_non_sad',  'tonal_atonal_atonal', 'voice_gender_male', 
                         'voice_instrumental_instrumental', 'Nsynth_Reverb_dry']

rename_labels = {'danceability_danceable':'danceability', 'mood_acoustic_acoustic':'mood_acoustic', 'mood_aggressive_aggressive':'mood_aggressive', 
                 'mood_electronic_electronic':'mood_electronic', 'mood_happy_happy':'mood_happy', 'mood_party_party':'mood_party', 'mood_relaxed_relaxed':'mood_relaxed', 
                 'mood_sad_sad':'mood_sad', 'voice_instrumental_voice':'overall_voice', 'voice_gender_female':'voice_female', 
                 'tonal_atonal_tonal':'tonal','Engagement_engagement':'Engagement', 'Nsynth_Reverb_wet':'Reverb_wet'
                 }
all_columns_to_drop = genre_to_drop + tags_to_drop + instruments_to_drop + other_columns_to_drop

if len(audio_file_list) > 0:
    column_labels, rows = extract_all_features(audio_file_list)
    new_df = pd.DataFrame(rows, columns=column_labels)

    new_df.drop(columns=all_columns_to_drop, inplace=True)
    new_df.rename(columns=rename_labels, inplace=True)

    genre_columns = [col for col in new_df.columns if col.startswith("Genre")]
    tag_columns = [col for col in new_df.columns if col.startswith("Tag")]

    genre_data = new_df[genre_columns].T
    tag_data = new_df[tag_columns].T

    top_genres, top_tags = [], []
    for col in genre_data.columns:
        temp1 = genre_data[col].nlargest(3).index.to_list()
        temp2 = tag_data[col].nlargest(5).index.to_list()
        top_genres.append(temp1)
        top_tags.append(temp2)

    new_df['top_genres'] = top_genres
    new_df['top_tags'] = top_tags

    right_exclusive_join = new_df['song name'][~new_df['song name'].isin(df_features['song name'])]
    new_entries = new_df[new_df['song name'].isin(right_exclusive_join)]

    updated_dataframe = pd.concat([df_features, new_entries], ignore_index=True)
    updated_dataframe.sort_values('song name', inplace=True)
    updated_dataframe.reset_index(drop=True, inplace=True)

    updated_dataframe['song name'].to_frame().to_csv('data/processed_songs.csv', index=False)
    updated_dataframe.to_csv('data/song_dataset_final.csv', index=False)
else:
    print("No new songs to extract")

