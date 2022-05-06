from flask import Flask, request
import random
from gevent.pywsgi import WSGIServer

from kinopoisk import get_movie
from decouple import config as cfg
from alice_images import upload_image, delete_uploaded_image, uploaded_images_list
from act_dict import base_dict


app = Flask(__name__)

word_list = base_dict()
hello_answer = word_list['hello_words']
bye_answer = word_list['bye_words']
genres = word_list['movie_short_genres']  # корни жанров фильмов
genre_list = word_list['movie_genres']  # жанры
genre_error = word_list['genre_error']  # ошибка жанров
hello_word_req = word_list['hello_words_from_user']  # возможные слова приветствия от юзера
goodbye_word_req = word_list['goodbye_words_from_user']  # возможные слова прощания от юзера
misunderstands = word_list['misunderstands']  # слова недопонимания


def act_movie_checker(text, movie_genres):
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
    m_type = 'Фильм'

    # screen checker
    try:
        user_screen = request.json['meta']['interfaces']['screen']
        is_user_have_screen = True
    except KeyError:
        is_user_have_screen = False

    end = False
    movie_img = None
    genre_name = None

    specified_genre = act_movie_checker(text=text, movie_genres=genres)[-1]

    # checking for a goodbye request
    if text in goodbye_word_req:
        response_text = f'{random.choice(bye_answer)}'
        end = True

    # if only the genre value is set in the request -> elif will return func only for a genres
    elif act_movie_checker(text=text, movie_genres=genres)[0] is True:
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

        # show movie section
        try:
            l = []
            m = get_movie(genre_name)
            for i in m:
                l.append(i)

            try:
                movie = l[random.randint(0, len(l)-1)]
            except ValueError:
                movie = None

            # get image
            if movie.name_ru:
                m_name = movie.name_ru
            else:
                m_name = movie.name_original
            movie_img = upload_image(
                skill_id=cfg('SKILL_ID'),
                oauth_token=cfg("YANDEX_AUTH_TOKEN"),
                image_path_or_url=movie.poster_url,
            )
            if movie.type.name == 'FILM':
                m_type = 'фильм'
            elif movie.type.name == 'TV_SERIES':
                m_type = 'сериал'

            else:
                response_text = 'Извините, произошла какая-то ошибка.'
        except TypeError:
            response_text = genre_error[random.randint(0, len(genre_error)-1)]

        except AttributeError:
            response_text = genre_error[random.randint(0, len(genre_error)-1)]

    # checking for a hello request
    elif text in hello_word_req:
        response_text = f'{random.choice(hello_answer)}'

    # checking for misunderstands
    elif text:
        if text == 'помощь':
            response_text = 'Назовите жанр, который хотели бы увидеть.\n' \
                            'Скажите, например, Алиса, я хочу посмотреть боевик!'
        elif text == 'что ты умеешь' or text == 'что ты умеешь?' or text == 'что ты можешь' or text == 'что ты можешь?':
            response_text = f'Я покажу Вам фильм, по выбранному Вами жанру. Просто назовите тот жанр, который ' \
                            f'бы хотели посмотреть!'
        else:
            response_text = f'{misunderstands[random.randint(0, len(misunderstands)-1)]}'

    else:
        response_text = 'Привет, я посоветую тебе фильм, в зависимости от твоих жанровых предпочтений. ' \
                            'Просто скажи, в каком жанре ты бы хотел увидеть его и я найду для тебя' \
                            ' соответствующую картину.'

    if movie_img:
        response = {
            'response': {
                'text': response_text,
                "tts": f"{tts_response[random.randint(0, len(tts_response) - 1)]} Попробуйте глянуть {m_name}."
                       f" По данным Ай Эм Ди Би этот {m_type}"
                       f" набрал {movie.rating_imdb} баллов!",
                'buttons': [
                    {'title': 'Привет!', 'hide': True},
                    {'title': 'Помощь', 'hide': True},
                    {'title': 'Что ты умеешь?', 'hide': True},
                    {'title': 'Пока', 'hide': True},
                ],
                'card': {
                    'type': "ImageGallery",
                    'items': [
                        {
                            'image_id': movie_img['image']['id'],
                            'title': f'{m_name}',
                            'description': f'Рейтинг на IMDB: {movie.rating_imdb}',
                        },
                    ],
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
                    {'title': 'Помощь', 'hide': True},
                    {'title': 'Что ты умеешь?', 'hide': True},
                    {'title': 'Пока!', 'hide': True},
                ],

                'end_session': end,
            },
            'version': '1.0'
        }
    return response


for item in uploaded_images_list(skill_id=cfg('SKILL_ID'), oauth_token=cfg("YANDEX_AUTH_TOKEN"))['images']:
    delete_uploaded_image(skill_id=cfg('SKILL_ID'), oauth_token=cfg("YANDEX_AUTH_TOKEN"), image_id=item['id'])

if __name__ == '__main__':
    app.run('localhost', port=5000, debug=True)
    # http_server = WSGIServer(('', 5000), app)
    # http_server.serve_forever()
