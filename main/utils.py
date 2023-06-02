import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics.pairwise import cosine_similarity
from essentia.standard import  MonoLoader, TensorflowPredict2D, TensorflowPredictEffnetDiscogs
import numpy as np
from .models import Song, Genre, Tag
import json
from data.OpenL3_embeddings import EmbeddingsOpenL3
from main.choices import genre_weightage, tags_weightage, instrument_weightage, feature_weights
from pipeline_code import embedding_model_weights_dsg, embedding_model_weights_l3, all_columns_to_drop, rename_labels
import ast

def get_similar_songs_id(id):
    df = pd.read_csv('data/songs_db.csv')
    df_features = pd.read_csv('data/song_dataset_final.csv')
    merged_df = pd.merge(df, df_features, on='song name', how='inner')

    genre_columns = [col for col in merged_df.columns if col.startswith("Genre")]
    tag_columns = [col for col in merged_df.columns if col.startswith("Tag")]
    instrument_columns = [col for col in merged_df.columns if col.startswith("Instrument")]

    X = merged_df.iloc[:, 3:-2].copy()
    minmax = MinMaxScaler(feature_range=(0,1))
    X.iloc[:,:13] = minmax.fit_transform(X.iloc[:,:13])

    X['voice_male'] = (1- X['voice_female']) * X['overall_voice']
    X['voice_female'] = X['voice_female'] * X['overall_voice']

    for key in feature_weights:
        X[key] = X[key] * feature_weights[key]
    for col in genre_columns:
        X[col] = X[col] * genre_weightage
    for col in instrument_columns:
        X[col] = X[col] * instrument_weightage
    for col in tag_columns:
        X[col] = X[col] * tags_weightage

    df_cosine=pd.DataFrame(cosine_similarity(X, dense_output=True))
    indices = pd.Series(merged_df.index, index = merged_df['ID'])

    index = indices[id]
    similarity_scores = list(enumerate(df_cosine[index]))
    similarity_scores = sorted(similarity_scores, key = lambda x: x[1],reverse = True)
    similarity_scores = similarity_scores[1:16]
    res_indices = [i[0] for i in similarity_scores]
    return merged_df['ID'].iloc[res_indices[:]].to_list()


path = "data/all_classifiers_and_metadata/"
song_path = 'media/'

def extract_all_features(all_songs, df_extract):
    column_labels = ['song name']
    rows = []
    flag = True
    with open('data/weights_metadata.json') as json_file:
        model_weights_metadata = json.load(json_file)
    json_file.close()

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
            
        scores = [df_extract[df_extract['file_path'] == song]['song name'].values[0]]

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


def train_model():
    df_django = pd.read_csv('data/songs_db.csv')
    df_features = pd.read_csv('data/song_dataset_final.csv')

    processed_songs = pd.read_csv('data/processed_songs.csv')
    df_to_extract = df_django[~df_django['song name'].isin(processed_songs['song name'])]
    audio_file_list = df_to_extract['file_path']

    if len(audio_file_list) == 0:
        print("terminating")
        return
    column_labels, rows = extract_all_features(audio_file_list, df_to_extract)
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


def update_songs_in_database_to_csv():
    song_models = Song.objects.all()
    all_songs = []
    for song in song_models:
        temp = []
        temp.append(song.id)
        temp.append(song.original_filename)
        temp.append(song.audio_file.name)
        all_songs.append(temp)
    df = pd.DataFrame(all_songs, columns=['ID', 'song name', 'file_path'])
    df.sort_values('song name', inplace=True)
    df.to_csv('data/songs_db.csv', index=False)
    
def update_csv_files_upon_model_deletion():
    df_processed = pd.read_csv('data/processed_songs.csv')
    df_database = pd.read_csv('data/songs_db.csv')
    df_features = pd.read_csv('data/song_dataset_final.csv')
    indices_to_delete = df_processed['song name'][~df_processed['song name'].isin(df_database['song name'])].index
    indices_to_delete2 = df_features['song name'][~df_features['song name'].isin(df_database['song name'])].index
    df_processed.drop(indices_to_delete, inplace=True)
    df_features.drop(indices_to_delete2, inplace=True)
    df_processed.reset_index(drop=True, inplace=True)
    df_features.reset_index(drop=True, inplace=True)
    df_processed.to_csv('data/processed_songs.csv', index=False)
    df_features.to_csv('data/song_dataset_final.csv', index=False)


def fill_genres_and_tags():
    songs = Song.objects.all()
    #songs = songs[:6]
    
    df = pd.read_csv('data/song_dataset_final.csv')
    for song in songs:
        if df['song name'].isin([song.original_filename]).any():
            song.processed = True
            if Genre.objects.filter(song=song).count() == 0:
                song_data = df[df['song name'] == song.original_filename]
                top_genres = song_data['top_genres'].tolist()[0]
                top_genres = ast.literal_eval(top_genres)
                for genre in top_genres:
                    score = song_data[genre].values[0]
                    Genre.objects.create(name=genre, song=song, score=score)

            if Tag.objects.filter(song=song).count() == 0:
                song_data = df[df['song name'] == song.original_filename]
                top_tags = song_data['top_tags'].tolist()[0]
                top_tags = ast.literal_eval(top_tags)
                for tag in top_tags:
                    score = song_data[tag].values[0]
                    Tag.objects.create(name=tag, song=song, score=score)
        else:
            song.processed = False
        song.save()
