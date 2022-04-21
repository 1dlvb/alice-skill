from kinopoisk_unofficial.kinopoisk_api_client import KinopoiskApiClient
from kinopoisk_unofficial.model.filter_country import FilterCountry
from kinopoisk_unofficial.model.filter_order import FilterOrder
from kinopoisk_unofficial.request.films.film_search_by_filters_request import FilmSearchByFiltersRequest
from kinopoisk_unofficial.request.films.filters_request import FiltersRequest

from decouple import config as cfg
import codecs
from random import randint

api_client = KinopoiskApiClient(cfg("API_TOKEN2"))
path_for_genres_file = 'movie_genres.txt'


class ShowMovies:
    # returns name of genres from txt file
    def get_genres(self, path):
        with codecs.open(path, 'r', encoding='utf-8') as f:
            return [i[:-2] for i in f]

    # returns generator type of movies
    def get_list_of_movies(self, genre_name, rating_from=7, year_from=1900):
        request = FilmSearchByFiltersRequest()
        request.year_from = year_from
        request.rating_from = rating_from
        request.order = FilterOrder.NUM_VOTE

        try:
            request.page = randint(1, 15)
        except:
            request.page = randint(1, 5)

        response = api_client.films.send_film_search_by_filters_request(request)

        genre = response.items[0].genres[0].__class__(genre=genre_name)  # топорно, но должно сработать
        for film in response.items:
            if genre in film.genres:
                yield film
