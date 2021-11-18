import streamlit as st
import pandas as pd
import movieFinder

url = 'https://raw.githubusercontent.com/NicolaiThomassen/moviefinder/main/all_movies.pkl'
df = pd.read_pickle(url)
mf = movieFinder.imdb_moviefinder(df)

rating = st.slider("Minimum average rating", 0.0, 10.0, 6.0, 0.1)
rating_to = st.slider("Maximum average rating", 0.0, 10.0, 6.0, 0.1)
num_votes_from = st.slider("Minimum number of votes", 0, 200000, 5000, 1000)
genre = st.selectbox('Genre', df['genre1'].unique())
year_from = st.selectbox('Year from', list(range(1990, 2022)))
year_to = st.selectbox('Year to', list(range(1990, 2022)))

st.write("Awesome movies", mf.search_movies(
    year_from=year_from,
    year_to=year_to,
    genre=genre,
    num_votes_from=num_votes_from,
    average_rating_from=rating,
    average_rating_to=rating_to
)[
    ['originalTitle',
     'averageRating',
     'numVotes',
     'genre1',
     'genre2',
     'genre3']
].head(30))
