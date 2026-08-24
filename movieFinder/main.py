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

    # df = df.iloc[:500]
    providers = []
    languages = []

    for i, imdb_id in enumerate(df["titleId"], start=1):
        try:
            streaming, language = tmdb.get_streaming_info(imdb_id)

        except Exception as e:
            print(f"ERROR {imdb_id}: {e}", flush=True)
            streaming = []
            language = None

        providers.append(streaming)
        languages.append(language)

        if i % 100 == 0:
            print(
                f"TMDB: {i}/{len(df)} movies processed",
                flush=True
            )

    df["providers"] = providers
    df["language"] = languages

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