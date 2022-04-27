from kinopoisk_unofficial.kinopoisk_api_client import KinopoiskApiClient
from kinopoisk_unofficial.model.filter_country import FilterCountry
from kinopoisk_unofficial.model.filter_order import FilterOrder
from kinopoisk_unofficial.request.films.film_search_by_filters_request import FilmSearchByFiltersRequest
from kinopoisk_unofficial.request.films.filters_request import FiltersRequest

from decouple import config as cfg
import codecs
from random import randint
from act_dict import base_dict

api_client = KinopoiskApiClient(cfg("API_TOKEN"))
path_for_genres_file = base_dict()['movie_genres']


class ShowMovies:

    def get_genre_id(self, name):
        request = FiltersRequest()
        response = api_client.films.send_filters_request(request)

        if name in self.get_genres(path_for_genres_file):
            for item in response.genres:
                if name == item.genre:
                    return item

    def get_list_of_movies(self, genre_name, rating_from=7, year_from=1900):
        request = FilmSearchByFiltersRequest()
        request.year_from = year_from
        request.order = FilterOrder.NUM_VOTE

        request.page = randint(1, 10)
        response = api_client.films.send_film_search_by_filters_request(request)
        for i in range(len(response.items)):
            for k in range(len(response.items[i].genres)):
                genre = response.items[i].genres[k].__class__(genre=genre_name)

        for film in response.items:
            if genre in film.genres:
                yield film
