import pandas as pd
class imdb_moviefinder:
    '''
    To use:
    run download_movies.store_movies()
    import pandas as pd
    df = pd.read_pickle('all_movies.pkl')
    '''
    def __init__(self, df):
        self.df = df
    
    def search_movies(self, year_from=None, year_to=None, genre=None, num_votes_from=None, average_rating_from=None):
        '''        
        genres: ['Comedy' 'Drama' 'Action' 'Animation' 'Horror' 'Biography' 'Adventure'
         'Documentary' 'Crime' 'Fantasy' 'Thriller' 'Mystery' 'Romance' 'Family'
         'Western' 'Musical' 'Sci-Fi' 'History' 'Music' 'Sport' 'War']
        '''
        if not year_from:
            year_from=self.df.startYear.min()
        
        if not year_to:
            year_to=self.df.startYear.max()
        
        if not average_rating_from:
            average_rating_from=self.df.averageRating.min()
        
        if not num_votes_from:
            num_votes_from=self.df.numVotes.min()
        
        movies = self.df.loc[(
            (self.df.startYear>=year_from) &
            (self.df.startYear<=year_to) &
            (self.df.averageRating>=average_rating_from) &
            (self.df.numVotes>=num_votes_from)
        )]
        
        if genre != None:
            movies = movies.loc[((self.df.isin([genre]).any(axis=1)))].copy()
        
        return movies.sort_values('averageRating', ascending=False)
    
    
    def get_release_month(self, movie_df):
        '''
        Add release months to found movies.
        '''
        from imdb import IMDb
        import datetime
        
        imdbDB = IMDb()
        movies = movie_df.loc[movie_df.startYear>=datetime.date.today().year-1].copy()
        
        if len(movies) == 0:
            return print(f'No movies newer than year {datetime.date.today().year-1}')
        
        movie_release = []
        for _, ids in movies.titleId.iteritems():
            movie = imdbDB.get_movie(ids.split('tt')[-1])
            try:
                movie_release.append(pd.to_datetime('-'.join(movie['original air date'].split(' ')[:3])))
            except:
                try: movie_release.append(pd.to_datetime('-'.join(movie['original air date'].split(' ')[:2])))
                except: movie_release.append(pd.to_datetime('-'.join(movie['original air date'].split(' ')[:1])))
                
        movies.loc[:, 'release'] = movie_release
        movies.loc[:, 'downloadable'] = list(movies.release.dt.date < datetime.date.today()-datetime.timedelta(90))
        return movies