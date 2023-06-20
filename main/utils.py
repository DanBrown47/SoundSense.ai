import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics.pairwise import cosine_similarity
from essentia.standard import MonoLoader, TensorflowPredict2D, TensorflowPredictEffnetDiscogs
from data.OpenL3_embeddings import EmbeddingsOpenL3
from main.choices import genre_weightage, tags_weightage, mdata_outliers, normalizing_factor, normalizing_factor_meta
from pipeline_code import embedding_model_weights_dsg, embedding_model_weights_l3, all_columns_to_drop, rename_labels
from unidecode import unidecode
from main import choices
from sklearn.feature_extraction.text import TfidfVectorizer
from .models import Song, Genre, Tag
import numpy as np
import music_tag
import json
import ast
import regex as re

def get_similar_songs_id(request, id):
    df = pd.read_csv('data/songs_db.csv')
    df_features = pd.read_csv('data/song_dataset_final.csv')
    meta_df = pd.read_csv('data/metadata.csv')
    df['year'] = meta_df['year']
    merged_df = pd.merge(df, df_features, on='song name', how='inner')
    
    genre_columns = [col for col in merged_df.columns if col.startswith("Genre")]
    tag_columns = [col for col in merged_df.columns if col.startswith("Tag")]
    instrument_columns = [col for col in merged_df.columns if col.startswith("Instrument")]
    
    X = merged_df.iloc[:, 3:-2].copy()
    X['year'] = X['year'].replace(0, np.nan).fillna(X['year'].median())
    minmax = MinMaxScaler(feature_range=(0,1))
    X.iloc[:,:14] = minmax.fit_transform(X.iloc[:,:14])

    X['voice_male'] = (1 - X['voice_female']) * X['overall_voice']
    X['voice_female'] = X['voice_female'] * X['overall_voice']

    instrument_weightage = choices.instrument_weightage
    feature_weights = choices.feature_weights
    balancing_factor = choices.balancing_factor

    if request.user.is_authenticated:
        pref = request.user.preference
        if pref:
            feature_weights['Engagement'] = pref.engagement
            feature_weights['danceability'] = pref.danceability
            feature_weights['mood_acoustic'] = pref.acoustics
            feature_weights['mood_aggressive'] = pref.aggressive
            feature_weights['mood_happy'] = pref.happy
            feature_weights['mood_party'] = pref.party
            feature_weights['mood_relaxed'] = pref.relaxed
            feature_weights['mood_sad'] = pref.sad
            feature_weights['tonal'] = pref.tonality
            feature_weights['Reverb_wet'] = pref.reverb
            feature_weights['voice_female'] = pref.gender
            feature_weights['voice_male'] = pref.gender
            feature_weights['overall_voice'] = pref.voice
            feature_weights['year'] = pref.year
            instrument_weightage = pref.instrument
            balancing_factor = pref.metadata

    for key in feature_weights:
        X[key] = X[key] * feature_weights[key]
    for col in genre_columns:
        X[col] = X[col] * genre_weightage
    for col in instrument_columns:
        X[col] = X[col] * instrument_weightage
    for col in tag_columns:
        X[col] = X[col] * tags_weightage

    df_cosine = pd.DataFrame(cosine_similarity(X, dense_output=True))
    df_cosine = df_cosine.applymap(lambda x: np.power(x, normalizing_factor))
    indices = pd.Series(merged_df.index, index = merged_df['ID'])

    def remove_punct(text):
        return unidecode(re.sub(r'[^\w\s\,]', '', text.lower())) if str(text) != 'nan' else ''

    def remove_outliers_and_extra_space(text):
        for substring in mdata_outliers:
            text = text.replace(substring, '')
        clean_text = re.sub(r'\s+', ' ', text).strip()
        return clean_text
    
    artists = meta_df['artist'].apply(lambda x: remove_punct(x).split(', '))
    albums = meta_df['album'].apply(lambda x: remove_punct(x).split(', '))
    album_artist = meta_df['album artist'].apply(lambda x: remove_punct(x).split(', '))
    
    meta_df['artists_album'] = artists + album_artist + albums
    meta_df['artists_album'] = meta_df['artists_album'].apply(lambda x: [remove_outliers_and_extra_space(i) for i in x])
    meta_df['artists_album'] = meta_df['artists_album'].apply(lambda x: list(set(x)))
    meta_df['artists_album_final'] = meta_df['artists_album'].apply(lambda x: " ".join([text.replace(" ", "_") for text in x]))

    tfidf = TfidfVectorizer(stop_words = "english")
    tfidf_matrix = tfidf.fit_transform(meta_df['artists_album_final'])

    df_cosine_meta = pd.DataFrame(cosine_similarity(tfidf_matrix, tfidf_matrix))
    df_cosine_meta = df_cosine_meta.applymap(lambda x: np.power(x, normalizing_factor_meta) * balancing_factor)
    resultant_cosine = df_cosine.add(df_cosine_meta)

    index = indices[id]
    similarity_scores = list(enumerate(resultant_cosine[index]))
    similarity_scores = sorted(similarity_scores, key = lambda x: x[1],reverse = True)
    similarity_scores = similarity_scores[1:16]
    res_indices = [i[0] for i in similarity_scores]
    return merged_df['ID'].iloc[res_indices[:]].to_list()


path = "data/all_classifiers_and_metadata/"
song_path = 'media/'

def extract_all_features(all_songs, df_extract=None, single_file=None):
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
            
        scores = [song] if single_file else [df_extract[df_extract['file_path'] == song]['song name'].values[0]]

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
        print("no new songs to retrain. Terminating")
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
    df_metadata = pd.read_csv('data/metadata.csv')
    indices_to_delete = df_processed['song name'][~df_processed['song name'].isin(df_database['song name'])].index
    indices_to_delete2 = df_features['song name'][~df_features['song name'].isin(df_database['song name'])].index
    indices_to_delete3 = df_metadata['song name'][~df_metadata['song name'].isin(df_database['song name'])].index
    df_processed.drop(indices_to_delete, inplace=True)
    df_features.drop(indices_to_delete2, inplace=True)
    df_metadata.drop(indices_to_delete3, inplace=True)
    df_processed.reset_index(drop=True, inplace=True)
    df_features.reset_index(drop=True, inplace=True)
    df_processed.to_csv('data/processed_songs.csv', index=False)
    df_features.to_csv('data/song_dataset_final.csv', index=False)
    df_metadata.to_csv('data/metadata.csv', index=False)


def fill_genres_and_tags():
    songs = Song.objects.all()
    
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


def extract_metadata():
    all_songs = Song.objects.all()

    all_data = []
    for song in all_songs:
        temp = []
        audio_file = music_tag.load_file('media/' + song.audio_file.name)

        temp.append(song.original_filename)
        temp.append(str(audio_file['artist']))
        temp.append(str(audio_file['album']))
        temp.append(int(audio_file['tracknumber']))
        temp.append(str(audio_file['albumartist']))
        temp.append(int(audio_file['year']))
        all_data.append(temp)

    df_meta = pd.DataFrame(all_data)
    df_meta.columns = ['song name', 'artist', 'album', 'track no', 'album artist', 'year']
    df_meta.sort_values('song name', inplace=True)
    df_meta.to_csv('data/metadata.csv', index=False)


def upload_and_check_similarity(request, file_path = 'uploads/temp_neeraj.m4a'):
    df = pd.read_csv('data/songs_db.csv')
    df_features = pd.read_csv('data/song_dataset_final.csv')
    meta_df = pd.read_csv('data/metadata.csv')
    column_labels, rows = extract_all_features([file_path], single_file=file_path)
    new_df = pd.DataFrame(rows, columns=column_labels)
    new_df.drop(columns=all_columns_to_drop, inplace=True)
    new_df.rename(columns=rename_labels, inplace=True)

    genre_columns = [col for col in new_df.columns if col.startswith("Genre")]
    tag_columns = [col for col in new_df.columns if col.startswith("Tag")]
    instrument_columns = [col for col in new_df.columns if col.startswith("Instrument")]

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
    updated_dataframe = pd.concat([df_features, new_df], ignore_index=True)

    temp = []
    audio_file = music_tag.load_file(song_path + file_path)
    temp.append(file_path)
    temp.append(str(audio_file['artist']))
    temp.append(str(audio_file['album']))
    temp.append(int(audio_file['tracknumber']))
    temp.append(str(audio_file['albumartist']))
    temp.append(int(audio_file['year']))

    meta_df = pd.concat([meta_df, pd.DataFrame([temp], columns=meta_df.columns)], ignore_index=True)
    df = pd.concat([df, pd.DataFrame([[df['ID'].max() + 500, file_path, None]], columns=df.columns)], ignore_index=True)
    df['year'] = meta_df['year']
    merged_df = pd.merge(df, updated_dataframe, on='song name', how='outer')

    X = merged_df.iloc[:, 3:-2].copy()
    X['year'] = X['year'].replace(0, np.nan).fillna(X['year'].median())
    minmax = MinMaxScaler(feature_range=(0,1))
    X.iloc[:,:14] = minmax.fit_transform(X.iloc[:,:14])

    X['voice_male'] = (1 - X['voice_female']) * X['overall_voice']
    X['voice_female'] = X['voice_female'] * X['overall_voice']

    instrument_weightage = choices.instrument_weightage
    feature_weights = choices.feature_weights
    balancing_factor = choices.balancing_factor

    if request.user.is_authenticated:
        pref = request.user.preference
        if pref:
            feature_weights['Engagement'] = pref.engagement
            feature_weights['danceability'] = pref.danceability
            feature_weights['mood_acoustic'] = pref.acoustics
            feature_weights['mood_aggressive'] = pref.aggressive
            feature_weights['mood_happy'] = pref.happy
            feature_weights['mood_party'] = pref.party
            feature_weights['mood_relaxed'] = pref.relaxed
            feature_weights['mood_sad'] = pref.sad
            feature_weights['tonal'] = pref.tonality
            feature_weights['Reverb_wet'] = pref.reverb
            feature_weights['voice_female'] = pref.gender
            feature_weights['voice_male'] = pref.gender
            feature_weights['overall_voice'] = pref.voice
            feature_weights['year'] = pref.year
            instrument_weightage = pref.instrument
            balancing_factor = pref.metadata

    for key in feature_weights:
        X[key] = X[key] * feature_weights[key]
    for col in genre_columns:
        X[col] = X[col] * genre_weightage
    for col in instrument_columns:
        X[col] = X[col] * instrument_weightage
    for col in tag_columns:
        X[col] = X[col] * tags_weightage

    df_cosine = pd.DataFrame(cosine_similarity(X, dense_output=True))
    df_cosine = df_cosine.applymap(lambda x: np.power(x, normalizing_factor))
    indices = pd.Series(merged_df.index, index = merged_df['song name'])

    def remove_punct(text):
        return unidecode(re.sub(r'[^\w\s\,]', '', text.lower())) if str(text) != 'nan' else ''

    def remove_outliers_and_extra_space(text):
        for substring in mdata_outliers:
            text = text.replace(substring, '')
        clean_text = re.sub(r'\s+', ' ', text).strip()
        return clean_text

    artists = meta_df['artist'].apply(lambda x: remove_punct(x).split(', '))
    albums = meta_df['album'].apply(lambda x: remove_punct(x).split(', '))
    album_artist = meta_df['album artist'].apply(lambda x: remove_punct(x).split(', '))

    meta_df['artists_album'] = artists + album_artist + albums
    meta_df['artists_album'] = meta_df['artists_album'].apply(lambda x: [remove_outliers_and_extra_space(i) for i in x])
    meta_df['artists_album'] = meta_df['artists_album'].apply(lambda x: list(set(x)))
    meta_df['artists_album_final'] = meta_df['artists_album'].apply(lambda x: " ".join([text.replace(" ", "_") for text in x]))

    tfidf = TfidfVectorizer(stop_words = "english")
    tfidf_matrix = tfidf.fit_transform(meta_df['artists_album_final'])

    df_cosine_meta = pd.DataFrame(cosine_similarity(tfidf_matrix, tfidf_matrix))
    df_cosine_meta = df_cosine_meta.applymap(lambda x: np.power(x, normalizing_factor_meta) * balancing_factor)
    resultant_cosine = df_cosine.add(df_cosine_meta)

    index = indices[file_path]
    similarity_scores = list(enumerate(resultant_cosine[index]))
    similarity_scores = sorted(similarity_scores, key = lambda x: x[1],reverse = True)
    similarity_scores = similarity_scores[1:16]
    res_indices = [i[0] for i in similarity_scores]
    return merged_df['ID'].iloc[res_indices[:]].to_list()