import streamlit as st 
import numpy as np
import matplotlib.pyplot as plt 
import seaborn as sns 
import pandas as pd 
import plotly.figure_factory as ff 
import plotly.express as px
from wordcloud import WordCloud

# @st.cache(suppress_st_warning=True)
def app():
    st.title("Acoustic Data Analysis")
    st.text("We present an in-depth analysis of the dataset")
    @st.cache
    def load_df():
        df = pd.read_csv("data/data.csv")
        return df 
    df = load_df()
    st.markdown("## 1. Distribution of popularity of songs")
    fig, ax = plt.subplots()
    sns.distplot(df.popularity, bins=20)
    st.pyplot(fig)
    corr = df.corr()
    fig = px.imshow(corr)
    st.markdown("## 2. Correlation between acoustic features in the data")
    st.plotly_chart(fig)

    st.markdown("## 3. Clustermap of acoustic feaatures")
    st.image('data/clustermap.png', width=600)

    st.markdown("## 4. How many songs are being indexed each year?")
    x = df.groupby('year')['id'].count()
    fig = px.line(x=x.index, y=x, title="Count of Tracks added each year")
    fig.update_layout(xaxis_title="Year", yaxis_title="Count")
    st.plotly_chart(fig)

    st.markdown("## 5. Temporal analysis of acoustic features over time")
    columns = ["acousticness","danceability","energy","speechiness","liveness","valence"]
    temp_df = pd.DataFrame()
    for col in columns:
        x = df.groupby('year')[col].mean()
        temp_df[col] = x
    st.line_chart(temp_df)
    del temp_df
    st.text("Tracks have become more Energetic and Danceable in the recent years. ")
    st.text("The loudness and tempo has also increased. The tracks have become less Acoustic")

    st.markdown("## 6. Dominant words in song titles")
    wc = WordCloud(height=200, width=400).generate(" ".join(df.name))
    fig, ax = plt.subplots()
    plt.imshow(wc)
    st.pyplot(fig)
    del wc 
