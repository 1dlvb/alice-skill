from kinopoisk_unofficial.kinopoisk_api_client import KinopoiskApiClient
from kinopoisk_unofficial.model.filter_country import FilterCountry
from kinopoisk_unofficial.model.filter_order import FilterOrder
from kinopoisk_unofficial.request.films.film_search_by_filters_request import FilmSearchByFiltersRequest
from kinopoisk_unofficial.request.films.filters_request import FiltersRequest

from decouple import config as cfg
import codecs

api_client = KinopoiskApiClient(cfg("API_TOKEN"))
path_for_genres_file = 'movie_genres.txt'

# request = FilmSearchByFiltersRequest()
# request.genres = ['боевик', ]
# request.order = FilterOrder.RATING
# request.add_country(FilterCountry(1, 'США'))

# response = api_client.films.send_film_search_by_filters_request(request)
# print(response)


def get_genres(path):
    with codecs.open(path, 'r', encoding='utf-8') as f:
        return [i[:-2] for i in f]


# print(get_genres(path='movie_genres.txt'))


# returns the id of a chosen genre from a genre name
def get_genre_id(name):
    try:
        request = FiltersRequest()
        response = api_client.films.send_filters_request(request)
    except:
        return None
    if name in get_genres(path_for_genres_file):
        for item in response.genres:
            if name == item.genre:
                return item

        # print(response.genres.FilterGenre.(name))
        print(f'you chose {name} genre!')


def get_list_of_movies(genre_name, rating_from=7, year_from=1900):
    request = FilmSearchByFiltersRequest()
    request.year_from = year_from
    request.rating_from = rating_from
    request.add_genre(get_genre_id(genre_name))
    request.order = FilterOrder.NUM_VOTE

    response = api_client.films.send_film_search_by_filters_request(request)

    for i in response.items:
        if i.name_ru is not None:
            print(i.name_ru)
        else:
            print(i.name_original)


get_list_of_movies('драма', year_from=2022)
