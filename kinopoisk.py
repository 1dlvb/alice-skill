from kinopoisk_unofficial.request.films.film_video_request import FilmVideoRequest


from decouple import config as cfg
import random

# imports for kinopoisk
from kinopoisk_unofficial.request.films.filters_request import FiltersRequest
from kinopoisk_unofficial.kinopoisk_api_client import KinopoiskApiClient
from kinopoisk_unofficial.model.filter_order import FilterOrder
from kinopoisk_unofficial.request.films.film_search_by_filters_request import FilmSearchByFiltersRequest


api_client = KinopoiskApiClient(cfg("API_TOKEN"))


def get_movie(genre_name):
    req_id = FiltersRequest()
    res_id = api_client.films.send_filters_request(req_id).genres
    genre = None
    for item in res_id:
        if item.genre == genre_name:
            genre = item

    request = FilmSearchByFiltersRequest()
    request.genres = [genre]
    request.year_from = 2000
    request.order = FilterOrder.NUM_VOTE
    request.page = random.randint(1, 20)

    response = api_client.films.send_film_search_by_filters_request(request)
    for item in response.items:
        for i in item.genres:
            if genre.genre in i.genre:
                yield item
