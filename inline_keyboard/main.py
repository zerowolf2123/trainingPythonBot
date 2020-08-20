from telegram import Bot, Update, InlineKeyboardButton, InlineKeyboardMarkup, ParseMode
from telegram.ext import Updater, CommandHandler, CallbackContext
from telegram.ext import CallbackQueryHandler
from telegram.utils.request import Request
from inline_keyboard.config import TG_TOKEN
from logging import getLogger

logger = getLogger(__name__)


def debug_requests(f):
    def inner(*args, **kwargs):
        try:
            logger.info(f'Обращение в функцию {f.__name__}')
            return f(*args, **kwargs)
        except:
            logger.exception(f'Ошибка в обработке {f.__name__}')
            raise
    return inner


# 1
def key_board_url():
    # Если у вас больше одной кнопки, то лучше сохранять их в одном списке
    keyboard = [
        # Обязательно объявлять кнопки во вложенных списках, иначе компилятор выдаст ошибку
        [
            # Это пример самого простого вункционала inline кнопок, при нажатии будет перекидывать по указанному url
            InlineKeyboardButton('Группа в вк', url='https://vk.com/learn_python_together')
        ],
        # Каждый новый вложенный список, это новая строка в сетке
        [
            InlineKeyboardButton('Моя страница', url='https://vk.com/juvotnoe')
        ]
    ]
    # Возвращаем сетку
    return InlineKeyboardMarkup(keyboard)


# 2
def key_board_callback():
    keyboard = [
        [
            # При нажатии на кнопку будет возвращаться событие 'right' для дальнейшей обработки
            InlineKeyboardButton('Отредактировать', callback_data='right'),
            InlineKeyboardButton('Новое сообщение', callback_data='new')
        ],
        [
            InlineKeyboardButton('Ваш id', callback_data='chat_id')
        ],
        [
            InlineKeyboardButton('Ещё ➡️', callback_data='more')
        ]
    ]
    return InlineKeyboardMarkup(keyboard)


# 2
def key_board_callback1():
    keyboard = [
        [
            InlineKeyboardButton('Назад ⬅️', callback_data='back')
        ]
    ]
    return InlineKeyboardMarkup(keyboard)


# 3
# Самый интересный и наиболее функциональный способ объявления кнопок, используя циклы
def key_board_din(value):
    keyboard = []
    # Будьте осторожнее с количеством строк сетки, в telegram оно ограничено (Проверьте сами)
    # В моем случае будет обрабатываться 3 строк, но их может быть и 2, и 1, и 0, на работу бота это никак не повлияет
    for i in range(len(value)):
        # В каждой итерации цикла объявляет новою строку сетки
        # Можно сделать вложенный цикл, если вам нужно несколько кнопок в одной строке
        keyboard.append([InlineKeyboardButton(value[i], callback_data=f'{i}')])
    return InlineKeyboardMarkup(keyboard)


def keyboard_callback_handler(update: Update, context: CallbackContext):
    # Обработчик всех кнопок
    # Во время нажатия на кнопку передает на сервер все индификаторы, для этого и нужно писать update.callback_query
    query = update.callback_query
    # с помощью data мы берем конкретно текст callback_data
    data = query.data
    chat_id = update.effective_message.chat_id
    # 2
    if data == 'right':
        # "Удалим" клавиатуру у прошлого сообщения
        # (на самом деле отредактируем его так, что текст останется тот же, а клавиатура пропадёт)
        # query.edit_message_text - нужно для измения сообщения в котором произошло нажатие
        query.edit_message_text(
            text='Отредактировали сообщение',
            # Удаляем сетку
            parse_mode=ParseMode.MARKDOWN
        )
        # Можно дополнить отправлением нового сообщения с inline кнопками которые будут хранить в себе url
    elif data == 'new':
        context.bot.send_message(
            text=f"В этом сообщении может быть что угодно",
            chat_id=chat_id,
            reply_markup=key_board_callback()
        )
    elif data == 'chat_id':
        query.edit_message_text(
            text=f'Ваш id - {chat_id}',
            parse_mode=ParseMode.MARKDOWN
        )
    elif data == 'more':
        query.edit_message_text(
            text='Здесь ничего нет',
            # Меняем сетку
            reply_markup=key_board_callback1()
        )
    elif data == 'back':
        query.edit_message_text(
            text='Пример работы кнопок',
            # Меняем назад сетку
            reply_markup=key_board_callback()
        )
    # 3
    elif data == '0':
        a = ['5', 'hello', '4']
        query.edit_message_text(
            text='Вы нажали на первую кнопку',
            # Обратите внимание что вам придется каждый раз передавать значения
            # Можете подключить базу данных и сохранять в нее последнее соостояние пользователя (То что пользователь передал; последнее нажатие и тд.)
            reply_markup=key_board_din(a)
        )
    elif data == '1':
        a = ['11', 'hallo']
        query.edit_message_text(
            text='Вы нажали на вторую кнопку',
            reply_markup=key_board_din(a)
        )
    elif data == '2':
        a = ['33', '33', '5', '1']
        query.edit_message_text(
            text='Вы нажали на третью кнопку',
            reply_markup=key_board_din(a)
        )


def start(update: Update, context: CallbackContext):
    update.effective_message.reply_text(text='''Добро пожаловать.
Сегодня разбираем inline кнопки.
Нажмите /help что бы узнать подробности''')


def do_help(update: Update, context: CallbackContext):
    update.effective_message.reply_text('''Список примеров:
/first - первая сетка кнопок (url)
/second - третья сетка кнопок (callback_data)
/third - четвертая сетка, динамически изменяемое количество кнопок (callback_data)''')


def do_url_keyboard(update: Update, context: CallbackContext):
    # 1
    '''Сетка прикрепляется конкретно к этому сообщению'''
    update.effective_message.reply_text('К этому сообщению прикреплена сетка кнопок: ',
                                        # Вызываем именно как функцию
                                        # Прикрепляет к сообщени сетку кнопок
                                        reply_markup=key_board_url())


def do_callback_keyboard(update: Update, context: CallbackContext):
    # 2
    update.effective_message.reply_text('''К этому сообщению прикреплены несколько кнопок, 
с возможностью пролистываения Вперед и Назад: ''',
                                        reply_markup=key_board_callback())


@debug_requests
def do_callback_din_keyboard(update: Update, context: CallbackContext):
    # 3
    update.effective_message.reply_text('''К этому сообщению прикреплены несколько кнопок, 
количество можно изменить: ''',
                                        # Передаем текст для кнопок в первый раз
                                        reply_markup=key_board_din(['3', '4', '5']))


def main():
    req = Request(connect_timeout=1.0,
                  read_timeout=1.5)
    bot = Bot(token=TG_TOKEN,
              request=req)
    updater = Updater(bot=bot,
                      use_context=True,)
    updater.dispatcher.add_handler(CommandHandler('help', do_help))
    updater.dispatcher.add_handler(CommandHandler('start', start))
    updater.dispatcher.add_handler(CommandHandler('first', do_url_keyboard))
    updater.dispatcher.add_handler(CommandHandler('second', do_callback_keyboard))
    updater.dispatcher.add_handler(CommandHandler('third', do_callback_din_keyboard))
    # С помощью CallbackQueryHandler мы обрабатываем все события при нажатии на кнопку, если указан callback_data
    updater.dispatcher.add_handler(CallbackQueryHandler(callback=keyboard_callback_handler))
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
