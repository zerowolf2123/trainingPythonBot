from telegram import Bot, Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext, ConversationHandler
from telegram.ext import CallbackQueryHandler
from telegram.utils.request import Request
from bot_reg.config import TG_TOKEN, valid_age
from bot_reg.database import get_subscribers_tg_names, start_db, add_subscribers, add_subscribers_info

FULL_NAME, GENDER, AGE = range(3)


"""
Вы можете реализовать замок регистрации, чтобы человек не смог зарегаться заново.
Реализация открывания этого замка через админку (В будущем покажу как ее настроить)
Получение id пользователей в админке и рассылка сообщений
"""


def get_keyboard():
    # Если в вашей панели кнопок больше одной строки то задавайте [[..., ...], [..., ..., ...]]
    keyboard = [
        [
            # Первой элемент это текст который будет отображаться на кнопке
            # Второй элемент это возвращаемое значение при нажатии на кнопку
            InlineKeyboardButton('Мужской', callback_data='man'),
            InlineKeyboardButton('Женский', callback_data='woman'),
            InlineKeyboardButton('Другой', callback_data='another'),
        ]
    ]
    # Возварщаем сетку кнопок
    return InlineKeyboardMarkup(keyboard)


# Здесь будет обрабатываться нажатия на кнопки
def keyboard_callback_handler(update: Update, context: CallbackContext):
    # Берем все данные о сообщении бота к которому прикреплена сетка кнопок
    query = update.callback_query
    # Сохраняем callback_data
    data = query.data
    chat_id = update.effective_message.chat_id
    if data == 'man':
        context.user_data[GENDER] = 'Мужской'
    elif data == 'woman':
        context.user_data[GENDER] = 'Женский'
    elif data == 'another':
        context.user_data[GENDER] = 'Другой'
    context.bot.send_message(
        text="Введите свой возраст",
        chat_id=chat_id,
    )


def do_start(update: Update, context: CallbackContext):
    user = update.effective_user.full_name
    chat_id = update.effective_user.id
    update.effective_message.reply_text(text='''Добро пожаловать в чат.
Воспользуйтесь командой /help чтобы узнать больше''')
    # Добавляем пользователя в базу данных, если его нет
    add_subscribers(tg_name=user,
                    user_id=chat_id)


def do_help(update: Update, context: CallbackContext):
    update.effective_message.reply_text(text='''На данный момент вам доступны следующие команды:

/help - помощь
/reg - регистрация (/cancel - для досрочного завершения)'''
                                        )


def do_reg(update: Update, context: CallbackContext):
    update.effective_message.reply_text(
        '''Вы начали регистрацию.
Введите имя и фамилию чтобы продолжить''',)
    # Возвращаем ключ элемента, функция которой должна вызваться следущей
    # Текст вашего сообщения при этом сохраняется
    return FULL_NAME


def gender_handler(update: Update, context: CallbackContext):
    # Получает и сохраняет имя переданное пользователем
    context.user_data[FULL_NAME] = update.effective_message.text
    update.effective_message.reply_text(
        '''Выберите ваш пол: 
''',
        # Прикрепляем сетку кнопок к сообщению
        reply_markup=get_keyboard()
    )
    return AGE


def finish_handler(update: Update, context: CallbackContext):
    chat_id = update.effective_user.id
    # Проверяет введенный возраст
    age = valid_age(text=update.effective_message.text)
    if age is None:
        update.effective_message.reply_text('Пожалуйста, вводите возраст корректно')
        return AGE
    context.user_data[AGE] = age
    # СОХРАНЕНИЯ В БАЗУ ДАННЫХ
    add_subscribers_info(user_id=chat_id,
                         full_name=context.user_data[FULL_NAME],
                         age=context.user_data[AGE],
                         gender=context.user_data[GENDER])
    update.effective_message.reply_text(f'''Поздравляю вы успешно прошли регистрацию
Вы - {context.user_data[FULL_NAME]}
Пол - {context.user_data[GENDER]} 
Возраст - {context.user_data[AGE]}''')
    # Завершает процесс, обязательно нужно писать в конце
    return ConversationHandler.END


# Досрочный выход
def cancel_handler(update: Update, context: CallbackContext):
    update.effective_message.reply_text('Вы досрочно завершили регистрацию, приятного вам дня')
    return ConversationHandler.END


def main():
    # Задает время на подключение
    req = Request(connect_timeout=1.0,
                  read_timeout=1.5)
    # Обязатльно нужно добавлять request
    bot = Bot(token=TG_TOKEN,
              request=req)
    updater = Updater(bot=bot,
                      use_context=True)
    start_db()
    # Текст каждого сообщения сначала попадает в этот блок
    conv_handler = ConversationHandler(
        # При сробатывании этой команды сработает весь ConversationHandler и запустит регистрацию
        # Все сообщения будут переходить в этот кусок кода, пока вы не завершите регистрацию или не выйдете досрочно
        entry_points=[
            CommandHandler('reg', do_reg)
        ],
        # Словарь состояний
        states={
            # Внутри может быть сколько угодно элементов
            FULL_NAME: [
                # pass_user_data нужен для сохранения состояния между запросами (Сохраняет переданные данные)
                MessageHandler(Filters.all, gender_handler, pass_user_data=True),
            ],
            AGE: [
                MessageHandler(Filters.all, finish_handler, pass_user_data=True)
            ]
        },
        # Позволяет досрочно выйти из регистрации
        fallbacks=[
            CommandHandler('cancel', cancel_handler)
        ]
        # entry_points, states и fallbacks нужно обязательно указывать
    )
    updater.dispatcher.add_handler(conv_handler)
    updater.dispatcher.add_handler(CommandHandler('start', do_start))
    updater.dispatcher.add_handler(CommandHandler('help', do_help))
    # Обработчик нажатий на кнопки
    updater.dispatcher.add_handler(CallbackQueryHandler(callback=keyboard_callback_handler))
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
