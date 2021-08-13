import requests
from pathlib import Path
from zipfile import ZipFile
import gzip
import shutil
import os
import pandas as pd

def store_movies(minyear = 1990, store_tsvs=False):
    url1 = 'https://datasets.imdbws.com/title.basics.tsv.gz'
    url2 = 'https://datasets.imdbws.com/title.akas.tsv.gz'
    url3 = 'https://datasets.imdbws.com/title.ratings.tsv.gz'
    urls = [url1, url2, url3]

    [open(f'{Path(url).name}', 'wb').write(requests.get(url, allow_redirects=True).content) for url in urls]

    for path in Path('').glob('*.gz'):
        with gzip.open(path, 'rb') as f_in:
            with open('-'.join(path.as_posix().split('.')[:2])+'.tsv', 'wb') as f_out:
                shutil.copyfileobj(f_in, f_out)

    for zipfile in Path('').glob('*.gz'):
        os.remove(zipfile)

    tsv1 = 'title-akas.tsv'
    tsv2 = 'title-basics.tsv'
    tsv3 = 'title-ratings.tsv'
    
    titles = pd.read_csv(tsv1, sep='\t', low_memory=False)
    basics = pd.read_csv(tsv2, sep='\t', low_memory=False)
    ratings = pd.read_csv(tsv3, sep='\t', low_memory=False)

    df = titles.merge(basics, left_on='titleId', right_on='tconst').merge(ratings, left_on='titleId', right_on='tconst')

    titles = []
    ratings = []
    basics = []

    df = df.loc[df.region=='US']
    df = df.loc[df.numVotes>1000]
    df = df.loc[df.titleType == 'movie']
    df = df.loc[df.startYear != '\\N']

    df['startYear'] = df.startYear.astype(int)
    df = df.loc[df.startYear > minyear]

    df[['genre1', 'genre2', 'genre3']] = df['genres'].str.split(',',expand=True)

    df.drop(['ordering', 'language', 'types', 'isOriginalTitle', 'tconst_x','primaryTitle', 'genres', 'tconst_y', 'attributes', 'endYear', 'isAdult' ], axis=1, inplace=True)
    df = df.loc[~df.titleId.duplicated()]
    df.to_pickle('all_movies.pkl')
    
    if not store_tsvs:
        for tsv in [tsv1, tsv2, tsv3]:
            os.remove(tsv)