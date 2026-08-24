import os
import requests


BASE_URL = "https://api.themoviedb.org/3"

HEADERS = {
    "Authorization": f"Bearer {os.environ['TMDB_TOKEN']}",
    "Accept": "application/json",
}


def get_providers(tmdb_id, country="DK"):
    response = requests.get(
        f"{BASE_URL}/movie/{tmdb_id}/watch/providers",
        headers=HEADERS,
        # verify=False
    )
    response.raise_for_status()

    return response.json()["results"].get(country, {})


def get_streaming_info(imdb_id, country="DK"):
    response = requests.get(
        f"{BASE_URL}/find/{imdb_id}",
        headers=HEADERS,
        params={"external_source": "imdb_id"},
    )
    response.raise_for_status()

    movies = response.json()["movie_results"]

    if not movies:
        return [], None

    movie = movies[0]

    providers = get_providers(
        movie["id"],
        country,
    )

    streaming = [
        provider["provider_name"]
        for provider in providers.get("flatrate", [])
    ]

    return streaming, movie["original_language"]