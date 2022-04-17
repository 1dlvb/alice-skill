
from alice_scripts import Skill, request, say, suggest

skill = Skill(__name__)

@skill.script
def run_script():
    yield say('Добрый день! Как вас зовут?')
    name = request.command

    yield say('Сколько вам лет?')
    while not request.matches(r'\d+'):
        yield say('Я вас не поняла. Скажите число')
    age = int(request.command)

    yield say('Вы любите кошек или собак?',
              suggest('Обожаю кошечек', 'Люблю собак'))
    while not request.has_lemmas('кошка', 'кошечка',
                                 'собака', 'собачка'):
        yield say('У вас только два варианта - кошки или собаки.')
    loves_cats = request.has_lemmas('кошка', 'кошечка')

    yield say(f'Рада познакомиться, {name}! Когда вам '
              f'исполнится {age + 1}, я могу подарить '
              f'{"котёнка" if loves_cats else "щенка"}!',
              end_session=True)

#
# if __name__ == "__main__":
#     skill.run()















# from dialogic.dialog_connector import DialogConnector
# from dialogic.dialog_manager import TurnDialogManager
# from dialogic.server.flask_server import FlaskServer
# from dialogic.cascade import DialogTurn, Cascade
#
# csc = Cascade()
#
#
# @csc.add_handler(priority=10, regexp='(hello|hi|привет|здравствуй)')
# def hello(turn: DialogTurn):
#     turn.response_text = 'Привет! Это единственная условная ветка диалога.'
#
#
# @csc.add_handler(priority=1)
# def fallback(turn: DialogTurn):
#     turn.response_text = 'Я вас не понял. Скажите мне "Привет"!'
#     turn.suggests.append('привет')
#
#
# dm = TurnDialogManager(cascade=csc)
# connector = DialogConnector(dialog_manager=dm)
# server = FlaskServer(connector=connector)
#
# if __name__ == '__main__':
#     server.parse_args_and_run()