import requests

from cinematch_back.settings import Settings


def get_recommendation_by_id(movieId):
    url = f"https://api.themoviedb.org/3/movie/{movieId}/recommendations?language=pt-BR&page=1"
    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {Settings().TMDB_API_KEY}"
    }
    response = requests.get(url, headers=headers)
    return response.json()


def get_recommendation_series_by_id(serieId):
    url = f"https://api.themoviedb.org/3/tv/{serieId}/recommendations?language=pt-BR&page=1"

    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {Settings().TMDB_API_KEY}"
    }

    response = requests.get(url, headers=headers)
    return response.json()
