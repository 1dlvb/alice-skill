from flask import Flask, request
import codecs
import random
import json

from kinopoisk import ShowMovies
from decouple import config as cfg
from alice_images import upload_image


app = Flask(__name__)

sm = ShowMovies()
movie_genres_path = 'movie_genres.txt'
movie_genres_str = ",".join(i for i in sm.get_genres(movie_genres_path))
movie_genres_list = [i for i in sm.get_genres(movie_genres_path)]


# gets path to the file of answers and activation words and return lists of them
def answers_and_requests(path):

    hello_words, goodbye_words, act_movies_words, movie_genres = [], [], [], []

    with codecs.open(path, 'r', encoding='utf-8') as f:
        for i in f:
            if i.split('/')[0] == '':
                hello_words.append(i.split('/')[1])
            if i.split('*')[0] == '':
                goodbye_words.append(i.split('*')[1])
            if i.split('~')[0] == '':
                act_movies_words.append(i.split('~')[1])
            if i.split('1')[0] == '':
                movie_genres.append(i.split('1')[1])

        # deleting useless characters
        for i in range(len(hello_words)):
            hello_words[i] = hello_words[i][:-2]
        for i in range(len(goodbye_words)):
            goodbye_words[i] = goodbye_words[i][:-2]
        for i in range(len(act_movies_words)):
            act_movies_words[i] = act_movies_words[i][:-2]
        for i in range(len(movie_genres)):
            movie_genres[i] = movie_genres[i][:-2]

    return hello_words, goodbye_words, act_movies_words, movie_genres


def act_movie_checker(text, act_movies, movie_genres):
    movie_act_word_in_req = False
    movie_genre_in_req = False
    full_req = False
    genre = None

    # checking for the presence of some movie activation word in user request
    for act_movie in act_movies:
        if act_movie in text:
            print(f'act movie: {act_movie}')
            movie_act_word_in_req = True

    # checking for the presence of some movie genre activation word in the user request
    for movie_genre in movie_genres:
        if movie_genre in text:
            movie_genre_in_req = True
            genre = movie_genre
            # print(f'movie genre: {movie_genre}')

    # checking for full user request
    if movie_genre_in_req is True and movie_act_word_in_req is True:
        full_req = True
    return movie_act_word_in_req, movie_genre_in_req, full_req, genre


@app.route('/alice', methods=['POST'])
def resp():
    text = request.json.get('request', {}).get('command')
    end = False
    movie = []
    movie_img = None

    # possible user requests and alice answers
    hello_answer, bye_answer, act_movies, movie_genres = answers_and_requests('answers_and_activation_words.txt')

    bye_word_req = ['пока', 'пока-пока', 'покеда', 'до встречи', 'до скорых встреч', 'ну все, пока', 'выход',
                    'выйти', 'все пока', 'пока...']
    hello_word_req = ['привет', 'Здравсвуйте', 'здравствуй', 'привет-привет', 'приветик', 'здорова',
                      'добрый вечер', 'добрый день', 'доброе утро']

    is_full_movie_req = act_movie_checker(text=text, act_movies=act_movies, movie_genres=movie_genres)
    specified_genre = is_full_movie_req[3]
    # print(f'specified genre {specified_genre}')
    # print(is_full_movie_req)

    # checking for a goodbye request
    if text in bye_word_req:
        response_text = f'{random.choice(bye_answer)}'
        end = True

    # if movie request is fully filled (with genres and movie act. word) -> elif will return the movie and genres func
    elif is_full_movie_req[2] is True:
        print('Show movie and genres func')
        response_text = 'Show movie and genres func'

    # if only the movie act. word value is set in the request -> elif will return func only for a movie act. word
    elif is_full_movie_req[0] is True:
        print('Show only movie func')
        response_text = 'Show only movie func'

    # if only the genre value is set in the request -> elif will return func only for a genres
    elif is_full_movie_req[1] is True:
        for mg_item in movie_genres_list:
            if specified_genre in mg_item:
                genre_name = mg_item
                # print(f'You chose {genre_name} genre')

                movies = sm.get_list_of_movies(genre_name)
                for item in movies:
                    if item:
                        movie.append(item)
                    else:
                        print('error')

                for i in movie:

                    print(i.name_ru)
                    movie_img_url = i.poster_url_preview
                    movie_img = upload_image(
                        skill_id=cfg('SKILL_ID'),
                        oauth_token=cfg("YANDEX_AUTH_TOKEN"),
                        image_path_or_url=movie_img_url,
                    )
                    m_title = i.name_ru
                    m_rating = i.rating_imdb
                    print(i.type.name)
                    if i.type.name == 'FILM':
                        m_type = 'фильм'
                    elif i.type.name == 'TV_SERIES':
                        m_type = 'сериал'

                    response_text = 'Связываюсь с сервером... Передаю запрос... Жду ответ... Готово!'

                    break
                else:
                    response_text = 'Извините! У меня возникла какая-то ошибка!' \
                                    ' Попробуйте пока выбрать что-нибудь другое!'
                    break

        else:
            response_text = 'Похоже, что такого жанра пока нет в моем списке.'

        print('Show only genres func')

    # checking for a hello request
    elif text in hello_word_req:
        response_text = f'{random.choice(hello_answer)}'

    else:
        response_text = 'Скажите что-нибудь интересное, и я вам как-нибудь интересно отвечу!'
        # response_text = 'Извините! Я Вас не поняла, повторите пожалуйста.'

    if movie_img:
        response = {
            'response': {
                'text': response_text,
                "tts": f"Связываюсь с сервером... sil <[1700]>  Жду ответ... sil <[1700]>"
                       f" Готово! sil <[800]> Попробуйте глянуть {m_title}. По данным Ай Эм Ди Би этот {m_type} набрал {m_rating} баллов!",
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