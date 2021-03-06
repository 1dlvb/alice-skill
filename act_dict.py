def base_dict():
    base = {
        "bye_words": [
            "Пока-пока!",
            "До свидания!",
            "Если вы достаточно сильны, чтобы попрощаться, жизнь вознаградит вас новым приветом.",
            "Я начала скучать по Вам, как только Вы сказали до свидания.",
            "Прощание причиняет боль, когда история не окончена и книга закрыта.",
            "До свидания. Только на сегодня. Не навсегда.",
            "Надеюсь скоро увидимся снова!",
            "Приятно было с вами поболтать!",
            "Увидимся.",
            "Рада была вам помочь!"
        ],
        "hello_words": [
            "Здравствуйте",
            "Здравствуйте!",
            "Приветствую Вас!",
            "Приятная встреча!",
            "Приветствую, Вы прекрасно выглядите!",
            "Привет-привет, Вы всё также прекрасны!",
            "Какая приятная неожиданность!",
            "Невозможно рада видеть Вас!",
            "Привет, Вы всё прекрасны!",
            "Привет-привет, много хорошего слышала о вас!",
            "Привет, Вы очаровываете с первого слова!",
            "Приветствую, Любая встреча — неслучайна!",
            "Привет. Ого, мне именно так вас и описывали!",
            "Привет, Вы потрясающе выглядите!"
        ],
        "hello_words_from_user": [
            'привет',
            'привет-привет',
            'привет - привет',
            'привет привет',
            'приветик',
            'приветули',
            'прив',
            'привет, - говорю',
            'привет, - говорят',
            'привет, - говорим',
            'привет говорю',
            'привет говорят',
            'привет говорим',

            'здравствуй',
            'Здравсвуйте',
            'здравствуйте-здравствуйте',
            'здравствуйте - здравствуйте',
            'здравствуйте здравствуйте',
            'здравствуйте много о вас слышал',
            'здравствуйте давно не виделись',

            'здорово',
            'здорова',
            'здарова',
            'здарово',

            'добрый вечер',
            'добрый день',
            'доброе утро',
            'вечер в хату',
            'давно не виделись',

            'ку',
            'чё каво',
            'хеллоу',
            'хай',
            'hi',
            'Good morning',
            'hello',
            'моё почтение',
            'мое почтение',
            'салам',
            'салам алейкум',
            'салам пополам',
            'шалом',

            'горячо приветствую',
            'позвольте вас приветствовать',
            'позвольте вас поприветствовать',
            'приветствую',

            'рад вас приветствовать',
            'рада вас приветствовать',
            'рады вас приветствовать',

            'рад вас поприветствовать',
            'рада вас поприветствовать',
            'рады вас поприветствовать',

            'хочу выразить пламенный привет',

        ],

        "goodbye_words_from_user": [
            'пока',
            'пока-пока',
            'пока - пока',
            'пока пока',
            'покеда',
            'прощай',

            'до встречи',
            'до скорых встреч',
            'до следущей встречи',
            'до вечера',
            'до завтра',
            'до свидания',
            'все до свидания',
            'все до свиданья',

            'ну все пока',
            'ну все, пока',
            'ну все, давай пока',
            'ну все, давай, пока',
            'все давай, пока',
            'все давай, покеда',
            'все пока',
            'ну и все, давай пока',
            'ну все, давай пока',
            'ну все, давай пока значит',
            'ну и все, давай пока значит',
            'ну и все, ну и пока',
            'ну и все, ну пока',
            'пока, - говорю',
            'пока, - говорим',
            'пока, - говорят',
            'пока говорю',
            'пока говорим',
            'пока говорят',

            'чао',
            'чао какао',
            'всего хорошего',
            'спасибо за помощь',
            'разрешите откланяться',
            'позвольте откланяться',
            'счастливо',
            'всего хорошего',
            'всего доброго',

            'выход',
            'выйти',

        ],
        "movie_short_genres": [
            "биограф",
            "боев",
            "вестерн",
            "воен",
            "детект",
            "детск",
            "для взрослых",
            "документальн",
            "драм",
            "игр",
            "истор",
            "комед",
            "концерт",
            "короткометраж",
            "криминал",
            "мелодр",
            "музык",
            "мюзикл",
            "новост",
            "приключен",
            "реальное",
            "ТВ",
            "семейн",
            "нуар",
            "спорт",
            "ток-шоу",
            "трил",
            "ужас",
            "фантаст",
            "церемон",
            "индий",
            "фэнтез",
            'мульт',
            'аниме',

        ],

        "movie_genres": [
            "биография",
            "спорт",
            "боевик",
            'для взрослых',
            'церемония',
            'документальный',
            'мультфильм',
            "вестерн",
            "военный",
            "детектив",
            "детский",
            "драма",
            "комедия",
            "история",
            "короткометражка",
            "криминал",
            "мелодрама",
            "мюзикл",
            "приключения",
            "семейный",
            "триллер",
            "ужасы",
            "фантастика",
            "фэнтези",
            "аниме",
        ],
        'genre_error':
            [
            'Похоже, что я пока не могу найти этот жанр. Попробуйте какой-нибудь другой!',
            'Хмм.. Я почему-то не могу найти этот жанр. Попробуйте пока другой, а я обязательно исправлюсь!',
            'Похоже, что-то пошло не так. Попробуйте выбрать другой жанр, а я пока все обдумаю.',
            'У меня почему-то возникли проблемы с поиском этого жанра. Попробуйте другой!',
        ],
        'user_have_screen_resp':
            [
            'Нашла!',
            'Похоже что-то есть!',
            'Вот!',
            'Хмм... Похоже я что-то нашла!',

        ],
        'user_havent_screen_resp':
            [
            'Ищу, что же вам посмотреть... sil <[1700]>  Уже почти нашла... sil <[1700]> Готово! sil <[950]>',
            'Связываюсь с коллегой sil <[1700]> Хмм... sil <[800]>',
            'Ищу для Вас фильм sil <[1700]> подождите ещё немного sil <[800]>',
            'Сейчас-сейчас! sil <[1700]> Уже нашла! sil <[500]>',
            'Пока ищу фильм, я расскажу Вам историю: sil <[1700]> а нет, уже не успею! sil <[800]>',

        ],
        'misunderstands':
            [
            'Извините! Кажется, я вас не поняла!',
            'Что-что?',
            'Простите?',
            'Кажется, я вас не поняла!',
            'Хм... Думаю, я вас неправильно поняла!',
            'Кажется, я что-то не расслышала!',
            'Извините?',
        ],
    }
    return base