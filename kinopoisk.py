from kinopoisk_unofficial.kinopoisk_api_client import KinopoiskApiClient
from kinopoisk_unofficial.model.filter_country import FilterCountry
from kinopoisk_unofficial.model.filter_order import FilterOrder
from kinopoisk_unofficial.request.films.film_search_by_filters_request import FilmSearchByFiltersRequest
from kinopoisk_unofficial.request.films.filters_request import FiltersRequest

from decouple import config as cfg
import codecs

api_client = KinopoiskApiClient(cfg("API_TOKEN"))
path_for_genres_file = 'movie_genres.txt'
#
# request = FilmSearchByFiltersRequest()
# request.genres = ['боевик', ]
# request.order = FilterOrder.RATING
# request.add_country(FilterCountry(1, 'США'))

# response = api_client.films.send_film_search_by_filters_request(request)
# print(response)


def answers_and_requests(path):
    """НЕ ЗАБЫТЬ ДОБАВИТЬ ВЫВОД ЖАНРА ФИЛЬМА/АКТИВАЦИОННОГО СЛОВА"""
    hello_words, goodbye_words, act_movies_words, movie_genres = [], [], [], []

    with codecs.open(path, 'r', encoding='utf-8') as f:
        for i in f:
            if i.split('1')[0] == '':
                movie_genres.append(i.split('1')[1])

        # deleting useless characters
        for i in range(len(movie_genres)):
            movie_genres[i] = movie_genres[i][:-2]

    return movie_genres


def get_genres(path):
    with codecs.open(path, 'r', encoding='utf-8') as f:
        return [i[:-2] for i in f]


# print(get_genres(path='movie_genres.txt'))
# request = FiltersRequest()
# response = api_client.films.send_filters_request(request)


def get_genre_id(name):
    if name in get_genres(path_for_genres_file):
        print(f'you chose {name} genre!')

get_genre_id('драму')