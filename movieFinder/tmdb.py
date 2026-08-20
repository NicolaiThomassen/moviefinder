import os
import requests


BASE_URL = "https://api.themoviedb.org/3"

headers = {
    "Authorization": f"Bearer {os.environ['TMDB_TOKEN']}",
    "Accept": "application/json",
}


def imdb_to_tmdb(imdb_id):
    response = requests.get(
        f"{BASE_URL}/find/{imdb_id}",
        headers=headers,
        params={"external_source": "imdb_id"},
    )
    response.raise_for_status()

    movies = response.json()["movie_results"]

    if not movies:
        return None

    return movies[0]["id"]


def get_providers(tmdb_id, country="DK"):
    response = requests.get(
        f"{BASE_URL}/movie/{tmdb_id}/watch/providers",
        headers=headers,
    )
    response.raise_for_status()

    return response.json()["results"].get(country, {})

def get_streaming_providers(imdb_id, country="DK"):
    tmdb_id = imdb_to_tmdb(imdb_id)

    if tmdb_id is None:
        return []

    providers = get_providers(tmdb_id, country)

    return [
        provider["provider_name"]
        for provider in providers.get("flatrate", [])
    ]


# print(imdb_to_tmdb('tt15239678'))
# print(get_providers(imdb_to_tmdb('tt15239678')))
