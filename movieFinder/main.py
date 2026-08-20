from movieFinder.download_movies import store_movies
from movieFinder.upload_github import upload_to_github
import pandas as pd
from movieFinder import tmdb

def main():
    print("STARTING DOWNLOAD", flush=True)

    store_movies()

    print("DOWNLOAD FINISHED", flush=True)
    

    print("STARTING TMDB LOOKUP", flush=True)

    df = pd.read_pickle("all_movies.pkl")

    providers = []

    for i, imdb_id in enumerate(df["titleId"], start=1):
        try:
            result = tmdb.get_streaming_providers(imdb_id)
        except Exception as e:
            print(f"ERROR {imdb_id}: {e}", flush=True)
            result = []

        providers.append(result)

        if i % 100 == 0:
            print(
                f"TMDB: {i}/{len(df)} movies processed",
                flush=True
            )

    df["providers"] = providers

    df.to_pickle(
        "all_movies.pkl",
        protocol=4
    )

    print("TMDB LOOKUP FINISHED", flush=True)
    
    print("STARTING GITHUB UPLOAD", flush=True)

    upload_to_github()

    print("GITHUB UPLOAD FINISHED", flush=True)


if __name__ == "__main__":
    main()