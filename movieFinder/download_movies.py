from pathlib import Path
import gzip
import shutil
import os
import requests
import pandas as pd


def store_movies(minyear=1990, store_tsvs=False):
    url1 = "https://datasets.imdbws.com/title.basics.tsv.gz"
    url2 = "https://datasets.imdbws.com/title.akas.tsv.gz"
    url3 = "https://datasets.imdbws.com/title.ratings.tsv.gz"
    # urls = [url1, url2, url3]

    def download_file(url, filename):
        response = requests.get(url, stream=True)
        response.raise_for_status()

        with open(filename, "wb") as f:
            for chunk in response.iter_content(chunk_size=1024 * 1024):
                if chunk:
                    f.write(chunk)


    download_file(url1, "title.basics.tsv.gz")
    download_file(url2, "title.akas.tsv.gz")
    download_file(url3, "title.ratings.tsv.gz")

    tsv1 = "title.akas.tsv.gz"
    tsv2 = "title.basics.tsv.gz"
    tsv3 = "title.ratings.tsv.gz"

    print("Reading title.akas in chunks...")

    title_chunks = []

    for chunk in pd.read_csv(
        tsv1,
        sep="\t",
        usecols=[
            "titleId",
            "title",
            "region",
            "ordering",
            "language",
            "types",
            "isOriginalTitle",
            "attributes",
        ],
        chunksize=250_000,
    ):
        chunk = chunk.loc[chunk["region"] == "US"]

        if not chunk.empty:
            title_chunks.append(chunk)

    titles = pd.concat(title_chunks, ignore_index=True)

    del title_chunks

    print(f"US titles: {len(titles)}")

    print("Reading title.basics in chunks...")

    basic_chunks = []

    for chunk in pd.read_csv(
        tsv2,
        sep="\t",
        usecols=[
            "tconst",
            "titleType",
            "primaryTitle",
            "originalTitle",
            "isAdult",
            "startYear",
            "endYear",
            "runtimeMinutes",
            "genres",
        ],
        chunksize=250_000,
    ):
        chunk = chunk.loc[
            (chunk["titleType"] == "movie") &
            (chunk["startYear"] != "\\N")
        ].copy()

        chunk["startYear"] = pd.to_numeric(
            chunk["startYear"],
            errors="coerce",
        )

        chunk = chunk.loc[chunk["startYear"] > minyear]

        if not chunk.empty:
            basic_chunks.append(chunk)

    basics = pd.concat(basic_chunks, ignore_index=True)

    del basic_chunks

    print(f"Movies after filter: {len(basics)}")

    basics = basics.loc[
        (basics["titleType"] == "movie") &
        (basics["startYear"] != "\\N")
    ]

    basics["startYear"] = pd.to_numeric(
        basics["startYear"], errors="coerce"
    )

    basics = basics.loc[basics["startYear"] > minyear]

    print(f"Movies after year/type filter: {len(basics)}")

    print("Reading title.ratings...")

    ratings = pd.read_csv(
        tsv3,
        sep="\t",
        usecols=["tconst", "averageRating", "numVotes"],
        dtype={
            "tconst": "string",
            "averageRating": "float32",
            "numVotes": "int32",
        },
    )

    ratings = ratings.loc[ratings["numVotes"] > 1000]

    print(f"Movies after rating filter: {len(ratings)}")

    print("Merging...")

    df = (
        titles
        .merge(
            basics,
            left_on="titleId",
            right_on="tconst",
            how="inner",
        )
        .merge(
            ratings,
            left_on="titleId",
            right_on="tconst",
            how="inner",
        )
    )

    print(f"Merged rows: {len(df)}")

    df[["genre1", "genre2", "genre3"]] = (
        df["genres"]
        .str.split(",", expand=True)
        .reindex(columns=[0, 1, 2])
    )

    df.drop(
        [
            "ordering",
            "language",
            "types",
            "isOriginalTitle",
            "tconst_x",
            "primaryTitle",
            "genres",
            "tconst_y",
            "attributes",
            "endYear",
            "isAdult",
        ],
        axis=1,
        inplace=True,
        errors="ignore",
    )

    df = df.loc[~df["titleId"].duplicated()]

    print("Writing all_movies.pkl...")
    print(df.columns.tolist())
    df.to_pickle("all_movies.pkl", protocol=4)

    print(f"Done. {len(df)} movies written.")

    if not store_tsvs:
        for tsv in [tsv1, tsv2, tsv3]:
            os.remove(tsv)