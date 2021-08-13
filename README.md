Repo made because I was frustrated with IMDB's search engine or lack hereof.

``` imdb_moviefinder``` makes use of year, rating, votes and genres to find movies of your liking. Use as you please.

A clean installation using jupyter lab as interactive interpreter can be done as so:


```conda create --name imdb python=3.9```

```conda activate imdb```

```pip install movieFinderIMDB==0.0.5```

```conda install jupyterlab```

From here I'd open jupyterlab and with ```jupyter lab``` and run the code below

```
import movieFinder
movieFinder.store_movies() # this may take a while as it downloads, unpacks and compress a couple of large files
import pandas as pd
df = pd.read_pickle('all_movies.pkl')
mf = movieFinder.imdb_moviefinder(df)
movies = mf.search_movies(year_from=2015, year_to=2021, genre='Sci-Fi', num_votes_from=100000, average_rating_from=7)
movies
```
This will show the some great movies from 2015 to 2021. Note that genres hold the following possibilities: 

```
genres: ['Comedy' 'Drama' 'Action' 'Animation' 'Horror' 'Biography' 'Adventure'
 'Documentary' 'Crime' 'Fantasy' 'Thriller' 'Mystery' 'Romance' 'Family'
 'Western' 'Musical' 'Sci-Fi' 'History' 'Music' 'Sport' 'War'] 
 ```
 
 
If interest exist you can add the release date to the dataframe as done below, beware though, that this might take a few minutes as it depends on IMDB's website itself. 


```mf.get_release_month(movies)```
