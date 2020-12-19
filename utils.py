import pandas as pd 

# song_pop = pd.read_csv("data/song_rec_pop.csv", converters={'Genres': eval})
def rank_artist_similarity(data, artist, genre_parameter):
    artist_data = data[data.artists == artist]
    artist_genres = set(*artist_data.genres)
    similarity_data = data.drop(artist_data.index)
    similarity_data.genres = similarity_data.genres.apply(lambda genres: list(set(genres).intersection(artist_genres)))
    similarity_lengths = similarity_data.genres.str.len()
    similarity_data = similarity_data.reindex(similarity_lengths[similarity_lengths >= genre_parameter].sort_values(ascending=False).index)
    similarity_data.rename(columns={'artists': f'Similar Artists to {artist}', 'genres': 'Similar Genres', 'popularity': 'Artist Popularity'}, inplace=True)
    similarity_data.drop(['Similar Genres'], axis=1, inplace=True)
    return similarity_data

def rank_song_similarity(data, song, artist, genre_parameter):
    
    song_and_artist_data = data[(data.Artist == artist) & (data['Song Name'] == song)].sort_values('Year')[0:1]  # this ensures the first song is picked, not any remasters
    artist_genres = set(*song_and_artist_data.Genres)

    similarity_data = data[~data.Artist.str.contains(artist)] # drops the artist from the dataframe
    
    similarity_data.Genres = similarity_data.Genres.apply(lambda Genres: list(set(Genres).intersection(artist_genres)))
    
    similarity_lengths = similarity_data.Genres.str.len()
    similarity_data = similarity_data.reindex(similarity_lengths[similarity_lengths >= genre_parameter].sort_values(ascending=False).index)
    
    # similarity_data = similarity_data[similarity_data['Song Decade'] == song_and_artist_data['Song Decade'].values[0]]
    
    similarity_data = similarity_data.sort_values(by ='Song Popularity', ascending = False)
    
    
    similarity_data.rename(columns={'Song Name': f'Similar Song to {song}', 'Genres' : 'Similar Genres'}, inplace=True)
    return similarity_data.head(30)