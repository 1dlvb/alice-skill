from flask import Flask, request
import random

from kinopoisk import ShowMovies
from decouple import config as cfg
from alice_images import upload_image
from act_dict import base_dict

app = Flask(__name__)

sm = ShowMovies()

word_list = base_dict()
hello_answer = word_list['hello_words']
bye_answer = word_list['bye_words']
act_movies_words = word_list['movies_activation_words']  # слова для вызова показа фильма
genres = word_list['movie_short_genres']  # корни жанров фильмов
genre_list = word_list['movie_genres']  # жанры
error_phrase = word_list['']

def act_movie_checker(text, act_movies, movie_genres):
    movie_genre_in_req = False
    genre = None

    # checking for the presence of some movie genre activation word in the user request
    for movie_genre in movie_genres:
        if movie_genre in text:
            movie_genre_in_req = True
            genre = movie_genre

    return movie_genre_in_req,  genre


@app.route('/alice', methods=['POST'])
def resp():
    text = request.json.get('request', {}).get('command')
    end = False
    movie_img = None
    genre_name = None

    # possible user requests and alice answers
    bye_word_req = ['пока', 'пока-пока', 'покеда', 'до встречи', 'до скорых встреч', 'ну все, пока', 'выход',
                    'выйти', 'все пока']
    hello_word_req = ['привет', 'Здравсвуйте', 'здравствуй', 'привет-привет', 'приветик', 'здорова',
                      'добрый вечер', 'добрый день', 'доброе утро']

    specified_genre = act_movie_checker(text=text, act_movies=act_movies_words, movie_genres=genres)[-1]

    # checking for a goodbye request
    if text in bye_word_req:
        response_text = random.choice(bye_answer)
        end = True

    # if only the genre value is set in the request -> elif will return func only for a genres
    elif act_movie_checker(text=text, act_movies=act_movies_words, movie_genres=genres)[0] is True:
        for genre in genre_list:
            if specified_genre in genre:
                genre_name = genre

        if genre_name is None:
            response_text = 'Похоже, что такого жанра нет в моём списке!'

        movies = sm.get_list_of_movies(genre_name)
        for item in movies:
            movie_img_url = item.poster_url_preview
            movie_img = upload_image(
                skill_id=cfg('SKILL_ID'),
                oauth_token=cfg("YANDEX_AUTH_TOKEN"),
                image_path_or_url=movie_img_url,
            )
            m_title = item.name_ru
            m_rating = item.rating_kinopoisk
            if item.type.name == 'FILM':
                m_type = 'фильм'
            elif item.type.name == 'TV_SERIES':
                m_type = 'сериал'

                response_text = 'Кажется я нашла, что же вам посмотреть!'
            else:
                response_text = random.choice(error_phrase)
            break
        response_text = 'Похоже, что возникла какая-то ошибка! Попробуйте какой-нибудь другой жанр.'

    # checking for a hello request
    elif text in hello_word_req:
        response_text = random.choice(hello_answer)

    else:
        response_text = 'Скажите что-нибудь интересное, и я вам как-нибудь интересно отвечу!'

    if movie_img:
        response = {
            'response': {
                'text': response_text,
                "tts": f"Ищу, что же вам посмотреть... sil <[1700]>  Уже почти нашла... sil <[1700]>"
                       f" Готово! sil <[950]> Попробуйте глянуть {m_title}. По данным Кинопоика этот {m_type}"
                       f" набрал {m_rating} баллов!",
                'buttons': [
                    {'title': 'Привет!', 'hide': True},
                    {'title': 'Я хочу посмотреть фильм!', 'hide': True},
                    {'title': 'Пока!', 'hide': True},
                ],
                'card': {
                    'type': "BigImage",
                    'image_id': movie_img['image']['id'],
                    'title': m_title,
                    'description': f'Рейтинг на IMDB: {m_rating}',

                },
                'end_session': end,
            },
            'version': '1.0'
        }

    else:
        response = {
            'response': {
                'text': response_text,
                'buttons': [
                    {'title': 'Привет!', 'hide': True},
                    {'title': 'Я хочу посмотреть фильм!', 'hide': True},
                    {'title': 'Пока!', 'hide': True},
                ],

                'end_session': end,
            },
            'version': '1.0'
        }
    return response


app.run('localhost', port=5000, debug=True)
