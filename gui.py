import streamlit as st
import pandas as pd
import movieFinder

url = 'https://raw.githubusercontent.com/NicolaiThomassen/moviefinder/main/all_movies.pkl'
df = pd.read_pickle(url)
df['genre'] = df[['genre1','genre2','genre3']].fillna("").agg(' '.join, axis=1)
mf = movieFinder.imdb_moviefinder(df)

df['Title'] = df[['titleId','title','originalTitle']].fillna("").agg('///'.join, axis=1)
def make_clickable(val):
    # target _blank to open new window
    url, titleid, title = val.split('///')
    return f'<a target="_blank" href="https://www.imdb.com/title/{url}/">{title+"/"+titleid}</a>'
df['Title'] = df.Title.apply(make_clickable)


rating = st.slider("Minimum average rating", 0.0, 10.0, 6.0, 0.1)

rating_to = st.slider("Maximum average rating", 0.0, 10.0, 10.0, 0.1)

num_votes_from = st.slider("Minimum number of votes", 0, 200000, 50000, 1000)

genres = list(df['genre1'].unique())
genres.extend((None,))
idx1 = genres.index(None)
genre = st.selectbox('Genre', genres, index=idx1)

yearsa = list(range(1990, 2025, 1))
yearsa.extend((None,))
idx2 = yearsa.index(None)
year_from = st.selectbox('Year from', yearsa, index=idx2)

yearsb = list(range(2024, 1990, -1))
yearsb.extend((None,))
idx3 = yearsb.index(None)
year_to = st.selectbox('Year to', yearsb, index=idx3)

st.write("Awesome movies", mf.search_movies(
    year_from=year_from,
    year_to=year_to,
    genre=genre,
    num_votes_from=num_votes_from,
    average_rating_from=rating,
    average_rating_to=rating_to
)[
    ['Title',
     'averageRating',
     'genre',
     'numVotes',
    'startYear']
].rename(columns={
    'Title': "Title",
    "genre": "Genre",
    'averageRating':'IMDB Rating',
    'numVotes':'Votes',
    'startYear':'Year'
}).reset_index(drop=True).head(30).to_html(escape=False),
         unsafe_allow_html=True)
