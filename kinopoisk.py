from kinopoisk_unofficial.kinopoisk_api_client import KinopoiskApiClient
from kinopoisk_unofficial.model.filter_order import FilterOrder
from kinopoisk_unofficial.request.films.film_search_by_filters_request import FilmSearchByFiltersRequest
from kinopoisk_unofficial.request.films.film_video_request import FilmVideoRequest


from decouple import config as cfg
from random import randint

api_client = KinopoiskApiClient(cfg("API_TOKEN"))


def get_list_of_movies(genre_name):
    request = FilmSearchByFiltersRequest()
    request.order = FilterOrder.NUM_VOTE

    request.page = randint(1, 10)
    response = api_client.films.send_film_search_by_filters_request(request)
    for i in range(len(response.items)):
        for k in range(len(response.items[i].genres)):
            genre = response.items[i].genres[k].__class__(genre_name)

    for film in response.items:
        if genre in film.genres:
            return film.kinopoisk_id

# get trailer of the movie
def get_trailer(movie_id):
    request = FilmVideoRequest(movie_id)
    response = api_client.films.send_film_video_request(request)
    for i in response.items:
        if ('Трейлер (русский язык)' in i.name) or ('Трейлер (дублированный)' in i.name):
            if 'widgets.kinopoisk.ru' in i.url or 'www.youtube.com' in i.url:
                return i.url
