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
hello_word_req = word_list['hello_words_from_user']  # возможные слова приветствия от юзера
goodbye_word_req = word_list['goodbye_words_from_user']  # возможные слова прощания от юзера
misunderstands = word_list['misunderstands']

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

    try:
        user_screen = request.json['meta']['interfaces']['screen']
        is_user_have_screen = True
    except KeyError:
        is_user_have_screen = False

    end = False
    movie_img = None
    genre_name = None

    specified_genre = act_movie_checker(text=text, act_movies=act_movies_words, movie_genres=genres)[-1]

    # checking for a goodbye request
    if text in goodbye_word_req:
        response_text = f'{random.choice(bye_answer)}'
        end = True

    # if only the genre value is set in the request -> elif will return func only for a genres
    elif act_movie_checker(text=text, act_movies=act_movies_words, movie_genres=genres)[0] is True:
        if is_user_have_screen:
            tts_response = base_dict()['user_have_screen_resp']
            response_text = 'Кажется нашла!'
        else:
            tts_response = base_dict()['user_havent_screen_resp']
            response_text = 'Хм...'

        for genre in genre_list:
            if specified_genre in genre:
                genre_name = genre

        if genre_name is None:
            response_text = 'Похоже, что такого жанра нет в моём списке!'

        movie = sm.get_list_of_movies(genre_name)
        try:
            movie_img = upload_image(
                skill_id=cfg('SKILL_ID'),
                oauth_token=cfg("YANDEX_AUTH_TOKEN"),
                image_path_or_url=movie.poster_url_preview,
            )

            if movie.type.name == 'FILM':
                m_type = 'фильм'
            elif movie.type.name == 'TV_SERIES':
                m_type = 'сериал'

            else:
                response_text = 'Извините, произошла какая-то ошибка.'
        except AttributeError:
            response_text = 'Похоже, что возникла какая-то ошибка! Попробуйте какой-нибудь другой жанр.'

    # checking for a hello request
    elif text in hello_word_req:
        response_text = f'{random.choice(hello_answer)}'

    elif text:
        response_text = misunderstands[random.randint(0, len(misunderstands)-1)]

    else:
        response_text = 'Выберите какой-нибудь жанр фильма!'

    if movie_img and tts_response and response_text:
        response = {
            'response': {
                'text': response_text,
                "tts": f"{tts_response[random.randint(0, len(tts_response) - 1)]} Попробуйте глянуть {movie.name_ru}. По данным Ай Эм Ди Би этот {m_type}"
                       f" набрал {movie.rating_imdb} баллов!",
                'buttons': [
                    {'title': 'Привет!', 'hide': True},
                    {'title': 'Пока!', 'hide': True},
                ],
                'card': {
                    'type': "BigImage",
                    'image_id': movie_img['image']['id'],
                    'title': movie.name_ru,
                    'description': f'Рейтинг на IMDB: {movie.rating_imdb}',

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
                    {'title': 'Пока!', 'hide': True},
                ],

                'end_session': end,
            },
            'version': '1.0'
        }
    return response


app.run('localhost', port=5000, debug=True)