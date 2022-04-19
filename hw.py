from flask import Flask, request
import codecs
import random
import json


app = Flask(__name__)


def answers_and_requests(path):
    hello_words, goodbye_words, act_movies_words, movie_genres = [], [], [], []

    with codecs.open(path, 'r', encoding='utf-8') as f:
        for i in f:
            # print(i.split('~'))
            # print(act_movies_words)
            # searching for goodbye or hello words
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

    for act_movie in act_movies:
        if act_movie in text:
            print(f'act movie: {act_movie}')
            movie_act_word_in_req = True

    for movie_genre in movie_genres:
        if movie_genre in text:
            movie_genre_in_req = True
            print(f'movie genre: {movie_genre}')

    if movie_genre_in_req is True and movie_act_word_in_req is True:
        full_req = True
    return movie_act_word_in_req, movie_genre_in_req, full_req


@app.route('/alice', methods=['POST'])
def resp():
    text = request.json.get('request', {}).get('command')
    end = False
    is_full_movie_req = False

    hello_answer, bye_answer, act_movies, movie_genres = answers_and_requests('activate_words.txt')

    bye_word_req = ['пока', 'пока-пока', 'покеда', 'до встречи', 'до скорых встреч', 'ну все, пока', 'выход',
                    'выйти', 'все пока']
    hello_word_req = ['привет', 'Здравсвуйте', 'здравствуй', 'привет-привет', 'приветик', 'здорова',
                      'добрый вечер', 'добрый день', 'доброе утро']
    is_full_movie_req = act_movie_checker(text=text, act_movies=act_movies, movie_genres=movie_genres)
    print(is_full_movie_req)


    if text in bye_word_req:
        response_text = f'{random.choice(bye_answer)}'
        end = True

    elif is_full_movie_req[2] is True:
        print('Show movie and genres func')
        response_text = 'Show movie and genres func'

    elif is_full_movie_req[0] is True:
        print('Show only movie func')
        response_text = 'Show only movie func'

    elif is_full_movie_req[1] is True:
        print('Show only genres func')
        response_text = 'Show only genres func'

    elif text in hello_word_req:
        response_text = f'{random.choice(hello_answer)}'
    else:
        response_text = 'Скажите что-нибудь и я интересно вам отвечу!'
        # response_text = 'Извините! Я Вас не поняла, повторите пожалуйста.'

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