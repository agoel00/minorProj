import streamlit as st
import numpy as np
import pandas as pd 
import joblib
import matplotlib.pyplot as plt
from utils import rank_artist_similarity, rank_song_similarity

def app():
    st.title('Analysing Music Through the Lens of Machine Learning')
    st.text('Minor Project 2020')
    st.text('Anmol Goel | Chaitanya Dagar | Saurabh Rai | Shekhar Tyagi')
    st.markdown("---")
    st.sidebar.title('Recommend Me')
    option = st.sidebar.selectbox(
        "Choose an option",
        ("Similar Artists", "Similar Songs")
    )
    @st.cache
    def load_artists_df():
        df = pd.read_csv('data/artist_rec.csv', converters={'genres': eval})
        df = df.drop(['Unnamed: 0'], axis=1)
        artists_list = df['artists'].unique()[25:]
        return artists_list, df
    artists_list, df = load_artists_df()
    artist = st.sidebar.selectbox('Select an artist', artists_list, index=6000)


    if option=="Similar Artists":
        # st.markdown("## Similar artists")        
        st.markdown("The similarity between artists A and B is computed using the common genres between artists")
        st.latex(r"""
            similarity(A,B) = \frac{|Genres_A \cap Genres_B|}{|Genres_A \cup Genres_B|}
        """)

        parameter = st.sidebar.slider("Parameter", 0, 6, value=2)
        similar_artists = rank_artist_similarity(df, artist, parameter)
        st.markdown("---")
        for i, row in similar_artists.iterrows():
            st.write("{}".format(row['Similar Artists to {}'.format(artist)]))
            st.progress(row['Artist Popularity'])
        st.dataframe(similar_artists)

    elif option=="Similar Songs":
        st.markdown("The similarity between songs A and B is computed using the following formula using acoustic features of song as its latent embedding")
        st.latex(r"""
            similarity(A, B) = \frac{\sum_{i=1}^{n} A_i \times B_i}{\sqrt{\sum_{i=1}^{n} A_i^2} \times \sqrt{\sum_{i=1}^{n} B_i^2}}
        """)
        @st.cache
        def load_songs_df():
            songs_df = pd.read_csv('data/song_rec_pop.csv', converters={'Genres': eval})
            songs_df = songs_df.drop(['Unnamed: 0'], axis=1)
            songs_list = songs_df[songs_df['Artist']==artist]['Song Name'].values
            return songs_list, songs_df
        songs_list, songs_df = load_songs_df()
        song = st.sidebar.selectbox("Select a song", songs_list)
        parameter = st.sidebar.slider("Parameter", 0, 6, value=2)
        similar_songs = rank_song_similarity(songs_df, song, artist, parameter)
        st.write(similar_songs)
        
